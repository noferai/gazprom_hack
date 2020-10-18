from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import RedirectView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from rest_framework import viewsets, views
from rest_framework.response import Response
from config.settings import SITE_TITLE, TITLE_DELIM
from ..utils import get_clean_next_url
from .models import Task, TaskState, Client, Transaction, MCC
from .serializers import TaskSerializer, ClientSerializer, MCCSerializer, TransactionSerializer
from decimal import Decimal
from .mixins import ValidationMixin, TaskMixin
from .forms import (
    TaskForm,
    TaskFilterForm,
)


class BaseListView(ListView):
    paginate_by = 10

    select_related = None
    prefetch_related = None

    def post(self, *args, **kwargs):
        url = self.request.get_full_path()

        if self.request.META.get("HTTP_X_FETCH") == "true":
            return JsonResponse(dict(url=url))
        else:
            return HttpResponseRedirect(url)

    def _build_filters(self, q):
        params = {}

        for part in (q or "").split():
            if ":" in part:
                field, value = part.split(":")
                try:
                    operator = self.filter_fields[field]
                    params[operator] = value
                except KeyError:
                    continue
            else:
                params["title__icontains"] = part

        return params

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "{}{}{}".format(self.model._meta.verbose_name_plural, TITLE_DELIM, SITE_TITLE)

        if self.request.GET.get("q") is not None:
            context["show_all_url"] = self.request.path

        return context

    def get_queryset(self):
        qs = self.model.objects

        q = self.request.GET.get("q")

        params = self._build_filters(q)

        if q is None:
            qs = qs.all()
        else:
            qs = qs.filter(**params)

        if self.select_related is not None:
            qs = qs.select_related(*self.select_related)

        if self.prefetch_related is not None:
            qs = qs.prefetch_related(*self.prefetch_related)

        return qs


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all().order_by("updated_at")


class ClientViewSet(viewsets.ModelViewSet):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()


class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()


class MCCViewSet(viewsets.ModelViewSet):
    serializer_class = MCCSerializer
    queryset = MCC.objects.all()


@method_decorator(login_required, name="dispatch")
class HomeView(RedirectView):
    url = reverse_lazy("tenders:task-list")


@method_decorator(login_required, name="dispatch")
class TaskDetailView(DetailView):
    model = Client

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "{}{}{}".format(self.get_object(), TITLE_DELIM, SITE_TITLE)
        return context

    def post(self, *args, **kwargs):
        params = self.request.POST.dict()

        if params.get("remove") == "yes":
            url = reverse_lazy("tenders:task-list")

            if self.request.META.get("HTTP_X_FETCH") == "true":
                return JsonResponse(dict(url=url))
            else:
                return HttpResponseRedirect(url)
        url = self.request.get_full_path()

        if self.request.META.get("HTTP_X_FETCH") == "true":
            return JsonResponse(dict(url=url))
        else:
            return HttpResponseRedirect(url)


@method_decorator(login_required, name="dispatch")
class TaskCreateView(TaskMixin, CreateView):
    form_class = TaskForm
    template_name = "tenders/client_form.html"

    def get_context_data(self, **kwargs):
        context = super(TaskCreateView, self).get_context_data(**kwargs)
        context["page_title"] = "Добавление задачи{}{}".format(TITLE_DELIM, SITE_TITLE)
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        formset = self.get_context_data()["formset"]
        with transaction.atomic():
            self.object = form.save()
            if formset["form"].is_valid():
                formset["form"].instance = self.object
                formset["form"].save()
        url = self.get_success_url()

        if self.request.META.get("HTTP_X_FETCH") == "true":
            return JsonResponse(dict(url=url))

        return response


@method_decorator(login_required, name="dispatch")
class TaskUpdateView(TaskMixin, ValidationMixin, UpdateView):
    model = Client
    form_class = TaskForm
    template_name = "tenders/client_form.html"

    def get_context_data(self, **kwargs):
        context = super(TaskUpdateView, self).get_context_data(**kwargs)
        context["page_title"] = "Редактирование {}{}{}".format(self.get_object(), TITLE_DELIM, SITE_TITLE)
        return context


@method_decorator(login_required, name="dispatch")
class TaskDeleteView(TaskMixin, DeleteView):
    model = Task

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


@method_decorator(login_required, name="dispatch")
class TaskList(BaseListView):
    model = Task

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filters_form"] = TaskFilterForm(self.request.POST)
        context["report_buttons"] = True
        return context


@login_required
def task_mark_as_done(request, pk):
    url = get_clean_next_url(request, reverse_lazy("tenders:task-list"))
    instance = get_object_or_404(Task, id=pk)
    if instance.state.stype != 2:
        instance.state = TaskState.objects.get(stype__exact=2)
        instance.save(update_fields=["state"])
    if request.META.get("HTTP_X_FETCH") == "true":
        return JsonResponse(dict(url=url))
    else:
        return HttpResponseRedirect(url)

    # ClientSerializer, MCCSerializer, TransactionSerializer


class CheckVklad:
    def check(self, client, servicesArray):
        money = Decimal(client["pCUR_eop"]) + Decimal(client["pCRD_eop"]) + Decimal(client["pSAV_eop"])
        if money > Decimal(0.5) * Decimal(client["sWork_S"]):
            servicesArray.append(
                {"type": "Вклад", "reason": "На счетах у клиента хранится денет больше 50% от зарплаты"}
            )
        if Decimal(client["tPOS_S"]) < Decimal(0.3) * Decimal(client["sWork_S"]):
            servicesArray.append({"type": "Вклад", "reason": "Траты меньше 30% от зарплаты"})


def sumByKat(dictions, category):
    counter = 0
    for diction in dictions:
        if diction["MCC description"] == category:
            counter += Decimal(diction["CARD_AMOUNT_EQV_CBR"])

    return counter


class CheckAuto:
    def check(self, client, trans, servicesArray):
        limuzins = sumByKat(trans, "Лимузины и такси")
        if limuzins > 30000:
            servicesArray.append({"type": "Авто кредит", "reason": 'Большие траты на категорию "Лимузины и такси"'})

        acesuary = sumByKat(trans, "Автозапчасти и аксессуары")
        to = sumByKat(trans, "Станции техобслуживания с дополнительными услугами или без")

        if acesuary > 10000 and to > 10000:
            servicesArray.append(
                {"type": "Авто кредит", "reason": "Большие траты на автозапчасти и станции техобслуживания"}
            )

        agent = sumByKat(trans, "Агентства по автотранспорту")
        if agent > 0:
            servicesArray.append(
                {"type": "Авто кредит", "reason": "В последнее время клиент много тратит на ангента по автотранспорту"}
            )


class MiliCard:
    def check(self, client, trans, servicesArray):
        avia = sumByKat(trans, "Авиалинии, авиакомпании - нигде больше не классифицированные")
        aeroflot = sumByKat(trans, "AEROFLOT")

        if avia + aeroflot > 30000:
            servicesArray.append({"type": "Мили", "reason": "В последнее время клиент часто стал летать"})

        hotels = sumByKat(trans, "Отели и мотели - нигде более не классифицированные")
        if hotels > 50000:
            servicesArray.append(
                {"type": "Мили", "reason": "В последнее время клиент часто стал арендовать номера в отелях"}
            )


class Investicii:
    def check(self, client, trans, servicesArray):
        fin = sumByKat(trans, "Финансовые учреждения – торговля и услуги")

        if fin > 10000:
            servicesArray.append(
                {
                    "type": "Инвестиционный счет",
                    "reason": "В последнее время клиент часто стал тратить в категории "
                    '"Финансовые учреждения – торговля и услуги"',
                }
            )


class Ipoteka:
    def check(self, client, trans, servicesArray):
        agent = sumByKat(trans, "Агенты недвижимости и менеджеры - Аренда")

        if agent > 20000:
            servicesArray.append(
                {
                    "type": "Ипотека",
                    "reason": "В последнее время клиент часто стал тратить в категории "
                    '"Агенты недвижимости и менеджеры - Аренда"',
                }
            )

        univ = sumByKat(trans, "Колледжи, университеты")

        if univ > 50000:
            servicesArray.append(
                {
                    "type": "Ипотека",
                    "reason": "В последнее время клиент стал тратить в категории " '"Колледжи, университеты"',
                }
            )


class HypotesisView(views.APIView):
    def get(self, request):
        client = Client.objects.get(pk=request.query_params["client_id"])
        trans = Transaction.objects.filter(client_id_id=request.query_params["client_id"])
        transInfo = MCC.objects.all()
        transInfo_s = MCCSerializer(transInfo, many=True)
        trans_s = TransactionSerializer(trans, many=True)
        client_s = ClientSerializer(client)

        for tran in trans_s.data:
            tran["MCC description"] = next(item for item in transInfo_s.data if item["id"] == tran["MCC_CD"])[
                "Description"
            ]

        servicesArray = []
        check = CheckVklad()
        check.check(client_s.data, servicesArray)
        check = CheckAuto()
        check.check(client_s.data, trans_s.data, servicesArray)
        check = MiliCard()
        check.check(client_s.data, trans_s.data, servicesArray)
        check = Investicii()
        check.check(client_s.data, trans_s.data, servicesArray)
        check = Ipoteka()
        check.check(client_s.data, trans_s.data, servicesArray)

        return Response(servicesArray)
