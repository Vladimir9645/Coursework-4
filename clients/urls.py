from django.urls import path
from . import views

urlpatterns = [
    # Список получателей
    path('', views.RecipientListView.as_view(), name='recipient-list'),

    # Детальная страница получателя
    path('<int:pk>/', views.RecipientDetailView.as_view(), name='recipient-detail'),

    # Создать получателя
    path('create/', views.RecipientCreateView.as_view(), name='recipient-create'),

    # Редактировать получателя
    path('<int:pk>/update/', views.RecipientUpdateView.as_view(), name='recipient-update'),

    # Удалить получателя
    path('<int:pk>/delete/', views.RecipientDeleteView.as_view(), name='recipient-delete'),
]
