from django.contrib.auth.forms import UserChangeForm, ReadOnlyPasswordHashField, AdminPasswordChangeForm
from django.utils.translation import gettext_lazy as _
from .models import User


class UserUpdateForm(UserChangeForm):
    password = ReadOnlyPasswordHashField(
        label=_("Password"),
        help_text=_(
            "Необработанные пароли не сохраняются, поэтому возможности увидеть пароль нет."
            "Вы можете изменить пароль, перейдя по "
            '<a href="{}?next=/staff/">этой ссылке</a>.'
        ),
    )

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "password")


class AdminPasswordUpdateForm(AdminPasswordChangeForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs["user"]
        super().__init__(*args, **kwargs)
