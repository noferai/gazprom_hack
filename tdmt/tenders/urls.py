from django.urls import path

from .views import (
    HomeView,
    TaskCreateView,
    TaskList,
    TaskUpdateView,
    TaskDeleteView,
    TaskDetailView,
    task_mark_as_done,
)

app_name = "tenders"

urlpatterns = [
    path("", HomeView.as_view(), name="index"),
    path("tasks/", TaskList.as_view(), name="task-list"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("tasks/add/", TaskCreateView.as_view(), name="task-add"),
    path("tasks/<int:pk>/edit/", TaskUpdateView.as_view(), name="task-edit"),
    path("tasks/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),
    path("tasks/<int:pk>/mark-done/", task_mark_as_done, name="task-done"),
]
