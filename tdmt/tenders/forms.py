from django.forms import ModelForm, Select, ChoiceField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML, Field
from django_crispy_bulma.layout import Row, Column
from config.settings import TRUE_FALSE_CHOICES
from .models import Task
from .formset import Formset

submit_cancel_buttons = HTML(
    '<div class="field is-grouped">'
    + '<div class="control"><button class="button is-link" type="submit"><span class="icon is-small"><i class="fas fa-save"></i></span><small>Сохранить</small></button></div>'
    + '<div class="control"><a class="button is-text" href="{{ next_url }}">Отмена</a></div>'
    + "</div>"
)


class FormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(FormSetHelper, self).__init__(*args, **kwargs)
        self.layout = Layout(
            HTML(
                "<label class='label'>Добавить товар к заказу "
                + "<span class='tooltip-b' has-tooltip-multiline data-tooltip='Оставьте пустым, если товар не нужен'>?</span>"
                + "</label>"
            ),
            Row(
                Column("type", "series1", "series2"),
                Column(Field("task", css_class="allowclear"), "quantity", "price_eu", "price_ru"),
                css_class="edit-view is-marginless",
            ),
        )
        self.form_tag = False


class TaskForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields["auth"].widget.attrs.update({"class": "allowclear"})
        self.fields["tn_returned"] = ChoiceField(
            choices=TRUE_FALSE_CHOICES, label="ТН возвращена", initial=[0], widget=Select(), required=True,
        )
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(Column("name", "comment", css_class="edit-view",), Column("paid", Formset("formset", "helper")),),
            submit_cancel_buttons,
        )

    class Meta:
        model = Task
        exclude = ("created_at", "updated_at", "sum_eu", "sum_ru", "rate")


class TaskFilterForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(TaskFilterForm, self).__init__(*args, **kwargs)
        for field_name in ["tender", "state", "auth", "tn_returned"]:
            self.fields[field_name].required = False
            self.fields[field_name].empty_label = ""
        self.fields["tn_returned"] = ChoiceField(
            choices=[("", ""), *TRUE_FALSE_CHOICES],
            label="ТН возвращена",
            required=False,
            widget=Select(
                attrs={
                    "onchange": 'filter_table("ТН возвращена", this.options[this.selectedIndex].innerText);',
                    "class": "allowclear",
                }
            ),
        )
        self.helper = FormHelper()
        self.helper.layout = Layout(Row(Column("state",), Column(), css_class="edit-view"))

    class Meta:
        model = Task
        fields = "state"
        widgets = {
            "state": Select(
                attrs={
                    "onchange": 'filter_table("Статус", this.options[this.selectedIndex].innerText);',
                    "class": "allowclear",
                }
            ),
        }
