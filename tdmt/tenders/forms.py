from django.forms import ModelForm, Select, Form, ChoiceField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML
from django_crispy_bulma.layout import Row, Column
from .models import Client


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
            Row(Column("name", "surname", "comment", css_class="edit-view",), Column("birthday", "age")),
            submit_cancel_buttons,
        )

    class Meta:
        model = Client
        exclude = (
            "created_at",
            "updated_at",
        )


class TaskFilterForm(Form):
    CHOICES = [("", ""), ("true", "true"), ("false", "false")]
    group_by = ChoiceField(
        label="Премиумный клиент?",
        choices=CHOICES,
        required=False,
        widget=Select(attrs={"onchange": "filter_table('is_premium', this.options[this.selectedIndex].innerText);"}),
    )
