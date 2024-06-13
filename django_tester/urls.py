from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('home/', include('users.urls')),
    path('ab_test/', include('users.urls')),
    path('save_test/', include('users.urls')),
    path('load_test/1/', include('users.urls')),
]
