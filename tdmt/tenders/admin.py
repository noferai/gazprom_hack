from django.contrib import admin

from django_admin_listfilter_dropdown.filters import ChoiceDropdownFilter


class TaskStateAdmin(admin.ModelAdmin):
    list_display = ("name", "stype")
    list_filter = [
        ("stype", ChoiceDropdownFilter),
    ]
