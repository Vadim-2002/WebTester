from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'role')


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label="Имя пользователя",
        max_length=150,
        widget=forms.TextInput(attrs={'autofocus': True})
    )
    password = forms.CharField(
        label="Пароль",
        strip=False,
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ('username', 'password')
