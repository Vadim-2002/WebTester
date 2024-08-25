from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
     path('', views.personal_account, name='personal_account'),
     path('create_test', views.create_test, name="create_test"),
     path('ab_test/', views.ab_test, name="ab_test"),
     path("signup/", views.SignUp.as_view(), name="signup"),
     path('save_test/', views.save_test, name='save_test'),
     path('my_tests/', views.my_tests, name='my_tests'),
     path('send_test/', views.send_test, name='send_test'),
     path('submit_test/', views.submit_test, name='submit_test'),
     path('test_results_detail/', views.test_results_detail, name='test_results_detail'),
     path('save_test_results/', views.save_test_results, name='save_test_results'),
     path('delete_test/', views.delete_test, name='delete_test'),
     path('personal_account/', views.personal_account, name='personal_account'),
     path('edit_profile/', views.edit_profile, name='edit_profile'),
     path('change_password/', auth_views.PasswordChangeView.as_view(
          template_name='users/change_password/change_password.html'),
          name='change_password'),
     path('change_password_done/', auth_views.PasswordChangeDoneView.as_view(
          template_name='users/change_password/change_password_done.html'),
          name='password_change_done')
]