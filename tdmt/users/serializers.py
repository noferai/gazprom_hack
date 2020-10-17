from rest_framework import serializers
from django.urls import reverse

from .models import User


class UserSerializer(serializers.ModelSerializer):
    DT_RowId = serializers.SerializerMethodField()
    DT_RowAttr = serializers.SerializerMethodField()
    links = serializers.SerializerMethodField()

    def get_links(self, obj):
        return {
            "view": reverse("users:detail", kwargs={"pk": obj.id}),
            "edit": reverse("users:edit", kwargs={"pk": obj.id}),
            "delete": reverse("users:delete", kwargs={"pk": obj.id}),
        }

    def get_DT_RowId(self, obj):
        return "row_%d" % obj.pk

    def get_DT_RowAttr(self, obj):
        return {"data-pk": obj.pk}

    class Meta:
        model = User
        fields = ("DT_RowId", "DT_RowAttr", "id", "first_name", "last_name", "email", "links")
