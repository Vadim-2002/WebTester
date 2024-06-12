from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .forms import CustomUserCreationForm


# Создаем здесь представления.

def home(request):
    return render(request, "users/home.html")


def ab_test(request):
    return render(request, "tests/ab_test.html")


class SignUp(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
