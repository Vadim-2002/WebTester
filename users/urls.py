from django.urls import path
from . import views


urlpatterns = [
     path('', views.home, name="home"),
     path('ab_test/', views.ab_test, name="ab_test"),
     path("signup/", views.SignUp.as_view(), name="signup"),
     path('save_test/', views.save_test, name='save_test'),
     path('my_tests/', views.my_tests, name='my_tests'),
]