from django.urls import path
from . import views

urlpatterns = [
    path('auth', views.auth, name='auth'),
    path('', views.dashboard, name='dashboard'),
    path('pointcloud', views.pointcloud, name='pointcloud'),
]