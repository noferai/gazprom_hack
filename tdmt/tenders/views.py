from itertools import groupby
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
from rest_framework import viewsets
from config.settings import SITE_TITLE, TITLE_DELIM
from ..utils import get_clean_next_url
from .models import Task, TaskState
from .serializers import TaskSerializer
from .mixins import ValidationMixin, TaskMixin
from .forms import (
    TenderForm,
    TaskForm,
    ProductForm,
    ProductTypeForm,
    AuthForm,
    TenderGroupByForm,
    TaskFilterForm,
    ProductFilterForm,
    AuthGroupByForm,
    ProductFormSet,
    FormSetHelper,
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
    queryset = Task.objects.select_related("tender")


@method_decorator(login_required, name="dispatch")
class HomeView(RedirectView):
    url = reverse_lazy("tenders:task-list")


@method_decorator(login_required, name="dispatch")
class TaskDetailView(DetailView):
    model = Task

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
    template_name = "tenders/task_form.html"

    def get_context_data(self, **kwargs):
        context = super(TaskCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            formset = {
                "form": ProductFormSet(self.request.POST),
                "prefix": "products",
                "title": "Добавить к заказу товары",
            }

        else:
            formset = {"form": ProductFormSet(), "prefix": "products", "title": "Добавить к заказу товары"}

        context["page_title"] = "Добавление заказа{}{}".format(TITLE_DELIM, SITE_TITLE)
        custom_context = {"formset": formset, "helper": FormSetHelper()}
        return {**context, **custom_context}

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
    model = Task
    form_class = TaskForm
    template_name = "tenders/task_form.html"

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
