from rest_framework import serializers
from django.urls import reverse
from .models import Task, TaskState, Client, Transaction, MCC


class FieldMixin(object):
    def get_field_names(self, *args, **kwargs):
        field_names = self.context.get("fields", None)
        if field_names:
            return field_names

        return super(FieldMixin, self).get_field_names(*args, **kwargs)


class TaskStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskState
        fields = ("slug", "name")


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    state = TaskStateSerializer()
    links = serializers.SerializerMethodField()

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
            "created_at",
            "updated_at",
            "links",
        )
        extra_kwargs = {
            "date": {"format": "%d.%m.%Y"},
            "created_at": {"format": "%d.%m.%Y"},
            "updated_at": {"format": "%d.%m.%Y"},
        }


class ClientSerializer(FieldMixin, serializers.ModelSerializer):
    links = serializers.SerializerMethodField()

    @staticmethod
    def get_links(obj):
        return {
            "edit": reverse("tenders:task-edit", kwargs={"pk": obj.id}),
            "view": reverse("tenders:task-detail", kwargs={"pk": obj.id}),
            "delete": reverse("tenders:task-delete", kwargs={"pk": obj.id}),
            "mark-done": reverse("tenders:task-done", kwargs={"pk": obj.id}),
        }

    class Meta:
        model = Client
        exclude = ()


class TransactionSerializer(FieldMixin, serializers.ModelSerializer):
    class Meta:
        model = Transaction
        exclude = ()


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        exclude = ()


class MCCSerializer(serializers.ModelSerializer):
    class Meta:
        model = MCC
        exclude = ()
