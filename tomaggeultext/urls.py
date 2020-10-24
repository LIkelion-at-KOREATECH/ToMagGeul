from django.urls import path
from tomaggeultext import views

urlpatterns = [
    path('', views.tmtext, name='main'),
    path('create/', views.tmtextcreate, name='create'),
    path('tmlist', views.tmlist, name='tmlist'),
    path('createseries/',views.tmseriescreate, name='createseries'),
]