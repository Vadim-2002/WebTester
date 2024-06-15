from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label='Имя пользователя',
        help_text='Обязательно. Не более 150 символов. Допускаются буквы, цифры и @/./+/-/_.',
        widget=forms.TextInput(attrs={'placeholder': 'Имя пользователя'})
    )
    email = forms.EmailField(
        label='Адрес электронной почты',
        widget=forms.EmailInput(attrs={'placeholder': 'Адрес электронной почты'})
    )
    password1 = forms.CharField(
        label='Пароль',
        help_text=(
            'Ваш пароль не должен быть слишком похож на другую вашу личную информацию. '
            'Ваш пароль должен содержать как минимум 8 символов. '
            'Ваш пароль не должен быть часто используемым. '
            'Ваш пароль не должен состоять только из цифр.'
        ),
        widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'})
    )
    password2 = forms.CharField(
        label='Подтверждение пароля',
        help_text='Введите пароль ещё раз для подтверждения.',
        widget=forms.PasswordInput(attrs={'placeholder': 'Подтверждение пароля'})
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


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
