from django.urls import path
from . import views


urlpatterns = [
     path('', views.home, name="home"),
     path('ab_test/', views.ab_test, name="ab_test"),
     path("signup/", views.SignUp.as_view(), name="signup"),
     path('save_test/', views.save_test, name='save_test'),
     path('my_tests/', views.my_tests, name='my_tests'),
     path('send_test/', views.send_test, name='send_test'),
     path('submit_test/', views.submit_test, name='submit_test'),
     path('test_results_detail/', views.test_results_detail, name='test_results_detail'),
]