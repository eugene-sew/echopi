from django.urls import path
from . import views

urlpatterns = [
    path('devices/', views.device_list, name='device-list'),
    path('devices/<int:pk>/', views.device_detail, name='device-detail'),
    path('token/', views.CustomAuthToken.as_view(), name='api-token-auth'),
    path('alerts/', views.alert_list, name='alert-list'),
    path('alerts/<int:pk>/', views.alert_detail, name='alert-detail'),
    path('deployments/', views.deployment_list, name='deployment-list'),
    path('deployments/<int:pk>/', views.deployment_detail, name='deployment-detail'),
]
