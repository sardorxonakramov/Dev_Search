from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import Skill

User = get_user_model()


class Avtomat_input:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for _, field in self.fields.items():
            field.widget.attrs.update(
                {
                    "class": "input input--text",
                }
            )


class UserRegisterForm(Avtomat_input, UserCreationForm):
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "password1", "password2"]


class SkillForm(Avtomat_input, ModelForm):
    class Meta:
        model = Skill
        fields = ["name", "discription"]


class UpdateAccountForm(Avtomat_input, ModelForm):
    class Meta:
        model = User
        exclude = [
            "password",
            "last_login",
            "user_permissions",
            "is_superuser",
            "groups",
            'is_staff',
            "is_active",
            "data_joined",
            "bio",
            'occupation'
        ]
