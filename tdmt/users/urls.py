# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from django.urls import path
from rest_framework import routers
from . import views

app_name = "users"

urlpatterns = [
    url(regex=r"^$", view=views.UserListView.as_view(), name="list"),
    url(regex=r"^~redirect/$", view=views.UserRedirectView.as_view(), name="redirect"),
    path("<int:pk>", views.UserDetailView.as_view(), name="detail"),
    url(regex=r"^~add/$", view=views.UserCreateView.as_view(), name="add"),
    path("<int:pk>/edit/", views.UserUpdateView.as_view(), name="edit"),
    path("<int:pk>/delete/", views.UserDeleteView.as_view(), name="delete"),
    path("<int:pk>/password/", views.UserPasswordUpdateView.as_view(), name="password-change"),
]
