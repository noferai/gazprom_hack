from __future__ import absolute_import, unicode_literals
from django.contrib.auth.hashers import make_password
from rest_framework import viewsets
from ..utils import get_clean_next_url
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse, reverse_lazy
from django.http import JsonResponse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView, CreateView, FormView, DeleteView
from .forms import UserUpdateForm, AdminPasswordUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from config.settings import SITE_TITLE, TITLE_DELIM
from .models import User
from ..tenders.models import Client, MCC, Transaction
from ..tenders.serializers import ClientSerializer, MCCSerializer, TransactionSerializer
from .serializers import UserSerializer
from rest_framework.decorators import api_view


class UserDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = User
    slug_field = "email"
    slug_url_kwarg = "id"

    def test_func(self):
        user = self.get_object()
        return self.request.user.is_staff or (user.pk == self.request.user.pk)


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"id": self.request.user.id})


class UserCreateView(LoginRequiredMixin, CreateView):
    fields = ["first_name", "last_name", "email", "password"]
    model = User

    def form_valid(self, form):
        response = super().form_valid(form)
        instance = form.save(commit=False)
        instance.password = make_password(instance.password)
        instance.save()
        url = self.get_success_url()
        if self.request.META.get("HTTP_X_FETCH") == "true":
            return JsonResponse(dict(url=url))
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Добавление пользователя{}{}".format(TITLE_DELIM, SITE_TITLE)
        return context

    @property
    def success_url(self):
        return get_clean_next_url(self.request, reverse_lazy("users:list"))


class UserUpdateView(LoginRequiredMixin, UpdateView):
    form_class = UserUpdateForm
    model = User

    def form_valid(self, form):
        response = super().form_valid(form)

        url = self.get_success_url()

        if self.request.META.get("HTTP_X_FETCH") == "true":
            return JsonResponse(dict(url=url))

        return response

    def get_context_data(self, **kwargs):
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        context["page_title"] = "Редактирование {}{}{}".format(self.get_object(), TITLE_DELIM, SITE_TITLE)
        return context

    @property
    def success_url(self):
        return get_clean_next_url(self.request, reverse_lazy("users:list"))


class UserPasswordUpdateView(LoginRequiredMixin, FormView):
    form_class = AdminPasswordUpdateForm
    template_name = "users/user_password.html"

    def get_form_kwargs(self):
        kwargs = super(UserPasswordUpdateView, self).get_form_kwargs()
        kwargs["user"] = User.objects.get(pk=self.kwargs["pk"])
        return kwargs

    def form_valid(self, form):
        url = self.get_success_url()
        instance = form.save(commit=False)
        instance.save()
        if self.request.META.get("HTTP_X_FETCH") == "true":
            return JsonResponse(dict(url=url))
        return super(UserPasswordUpdateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["employee"] = User.objects.get(pk=self.kwargs["pk"])
        context["page_title"] = "Изменение пароля{}{}".format(TITLE_DELIM, SITE_TITLE)
        return context

    @property
    def success_url(self):
        return get_clean_next_url(self.request, reverse_lazy("users:list"))


class UserListView(LoginRequiredMixin, ListView):
    model = User
    slug_field = "email"
    slug_url_kwarg = "id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Пользователи{}{}".format(TITLE_DELIM, SITE_TITLE)
        return context


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all().order_by("id")


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    @property
    def success_url(self):
        return get_clean_next_url(self.request, reverse_lazy("users:list"))
