from crispy_forms.layout import LayoutObject
from django.template.loader import render_to_string


class Formset(LayoutObject):
    def __init__(self, formset_context_name, helper_context_name=None, template=None, label=None):
        self.formset_context_name = formset_context_name
        self.helper_context_name = helper_context_name
        self.fields = []
        self.template = "formset.html"

    def render(self, form, form_style, context, **kwargs):
        formset = context.get(self.formset_context_name)
        helper = context.get(self.helper_context_name)
        if helper:
            helper.form_tag = False

        context.update({"formset": formset, "helper": helper})
        return render_to_string(self.template, context.flatten())
