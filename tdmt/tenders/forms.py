from django.forms import ModelForm, Select
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML
from django_crispy_bulma.layout import Row, Column
from .models import Task


submit_cancel_buttons = HTML(
    '<div class="field is-grouped">'
    + '<div class="control"><button class="button is-link" type="submit"><span class="icon is-small"><i class="fas fa-save"></i></span><small>Сохранить</small></button></div>'
    + '<div class="control"><a class="button is-text" href="{{ next_url }}">Отмена</a></div>'
    + "</div>"
)


class TaskForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(Column("name", "comment", css_class="edit-view",), Column()), submit_cancel_buttons,
        )

    class Meta:
        model = Task
        exclude = (
            "created_at",
            "updated_at",
        )


class TaskFilterForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(TaskFilterForm, self).__init__(*args, **kwargs)
        self.fields["state"].required = False
        self.fields["state"].empty_label = ""
        self.helper = FormHelper()
        self.helper.layout = Layout(Row(Column("state",), Column(), css_class="edit-view"))

    class Meta:
        model = Task
        fields = ("state",)
        widgets = {
            "state": Select(
                attrs={
                    "onchange": 'filter_table("Статус", this.options[this.selectedIndex].innerText);',
                    "class": "allowclear",
                }
            ),
        }
