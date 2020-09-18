from django.urls import path
from tomaggeultext import views

urlpatterns = [
    path('main/', views.tmtext, name='main'),
]