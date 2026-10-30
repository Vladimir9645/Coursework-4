from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),  # регистрация/вход/подтверждение почты

    # Главная страница — дашборд статистики
    path('', include('stats.urls')),

    # Приложения
    path('clients/', include('clients.urls')),
    path('mail_templates/', include('mail_templates.urls')),
    path('mailings/', include('mailings.urls')),
]

