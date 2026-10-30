from django.urls import path
from . import views

urlpatterns = [
    path('', views.MessageTemplateListView.as_view(), name='template-list'),
    path('<int:pk>/', views.MessageTemplateDetailView.as_view(), name='template-detail'),
    path('create/', views.MessageTemplateCreateView.as_view(), name='template-create'),
    path('<int:pk>/update/', views.MessageTemplateUpdateView.as_view(), name='template-update'),
    path('<int:pk>/delete/', views.MessageTemplateDeleteView.as_view(), name='template-delete'),
]
