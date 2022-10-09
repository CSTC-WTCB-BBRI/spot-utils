from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes, name='routes'),
    path('hello-spot/', views.helloSpot, name='hello-spot'),
]