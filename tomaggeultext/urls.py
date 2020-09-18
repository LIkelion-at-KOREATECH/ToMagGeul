from django.urls import path
from tomaggeultext import views

urlpatterns = [
    path('', views.tmtext, name='main'),
]