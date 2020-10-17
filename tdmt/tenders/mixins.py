from django.views.generic.edit import FormMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from ..utils import get_clean_next_url


class ValidationMixin(FormMixin):
    def form_valid(self, form):
        response = super().form_valid(form)
        url = self.get_success_url()
        if self.request.META.get("HTTP_X_FETCH") == "true":
            return JsonResponse(dict(url=url))
        return response


class TaskMixin(FormMixin):
    @property
    def success_url(self):
        return get_clean_next_url(self.request, reverse_lazy("tenders:task-list"))
