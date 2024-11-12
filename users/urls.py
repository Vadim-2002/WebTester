from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
     # Главная (стартовая) страница
     path('', views.main_page, name='main'),

     # Авторизация
     path("signup", views.SignUp.as_view(), name="signup"),
     path('logout', auth_views.LogoutView.as_view(), name='logout'),

     # Работа с тестами
     path('create_test', views.create_test, name="create_test"),
     path('ab_test', views.ab_test, name="ab_test"),
     path('save_test', views.save_test, name='save_test'),
     path('my_tests', views.my_tests, name='my_tests'),
     path('my_test/test_results_detail/<int:test_id>', views.test_results_detail, name='test_results_detail'),
     path('send_test', views.send_test, name='send_test'),
     path('submit_test', views.submit_test, name='submit_test'),
     path('save_test_results', views.save_test_results, name='save_test_results'),
     path('delete_test', views.delete_test, name='delete_test'),

     # Работа с личным кабинетом
     path('personal_account', views.personal_account, name='personal_account'),
     path('edit_profile', views.edit_profile, name='edit_profile'),

     # Изменение пароля
     path('change_password', auth_views.PasswordChangeView.as_view(
          template_name='users/change_password/change_password.html'),
          name='change_password'),
     path('change_password_done', auth_views.PasswordChangeDoneView.as_view(
          template_name='users/change_password/change_password_done.html'),
          name='password_change_done'),

     # Раздел Команда
     path('teams', views.team_list, name='teams'),
     path('teams/create/', views.create_team, name='create_team'),
     path('teams/delete/<int:team_id>/', views.delete_team, name='delete_team'),
     path('teams/<int:team_id>/', views.team_detail, name='team_detail'),

     # Работа с сообщениями
     path('messages/<int:recipient_id>/', views.messages_view, name='messages'),
     path('get_messages_ajax/<int:recipient_id>/', views.get_messages_ajax, name='get_messages_ajax'),
]