from django.urls import path
from tomaggeultext import views

urlpatterns = [
    path('', views.tmtext, name='main'),
    path('it_sounds_good/<int:tmt_id>',views.it_sounds_good, name='it_sounds_good'),
    path('tmtext_detail/<int:tmt_id>',views.tmtext_detail, name='tmtext_detail'),
]