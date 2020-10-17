from rest_framework import serializers
from django.urls import reverse
from .models import Task, TaskState


class TaskStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskState
        fields = ("slug", "name")


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    state = TaskStateSerializer()
    links = serializers.SerializerMethodField()

    @staticmethod
    def get_tn_returned(obj):
        if obj.tn_returned:
            return "Да"
        else:
            return "Нет"

    @staticmethod
    def get_links(obj):
        return {
            "edit": reverse("tenders:task-edit", kwargs={"pk": obj.id}),
            "view": reverse("tenders:task-detail", kwargs={"pk": obj.id}),
            "delete": reverse("tenders:task-delete", kwargs={"pk": obj.id}),
            "mark-done": reverse("tenders:task-done", kwargs={"pk": obj.id}),
        }

    class Meta:
        model = Task
        fields = (
            "id",
            "state",
            "comment",
            "date",
            "created_at",
            "updated_at",
            "links",
        )
        extra_kwargs = {
            "date": {"format": "%d.%m.%Y"},
            "created_at": {"format": "%d.%m.%Y"},
            "updated_at": {"format": "%d.%m.%Y"},
        }