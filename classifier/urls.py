from django.urls import path
from . import views

urlpatterns = [
    path('', views.detect_audio, name='detect_audio'),
]