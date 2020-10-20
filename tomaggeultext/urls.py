from django.urls import path
from tomaggeultext import views

urlpatterns = [
    path('', views.tmtext, name='main'),
    path('createText/', views.createText, name="createText"),
    path('create/', views.tmtextcreate, name='create'),
]