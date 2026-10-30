from django.urls import path
from . import views

urlpatterns = [
    path('', views.MailingListView.as_view(), name='mailing-list'),
    path('<int:pk>/', views.MailingDetailView.as_view(), name='mailing-detail'),
    path('create/', views.MailingCreateView.as_view(), name='mailing-create'),
    path('<int:pk>/update/', views.MailingUpdateView.as_view(), name='mailing-update'),
    path('<int:pk>/delete/', views.MailingDeleteView.as_view(), name='mailing-delete'),

    # Отдельная страница/действие для запуска рассылки (можно сделать через GET или POST)
    path('<int:pk>/send/', views.send_mailing_view, name='mailing-send'),
]
