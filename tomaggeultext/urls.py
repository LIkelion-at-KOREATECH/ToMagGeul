from django.urls import path
from tomaggeultext import views

urlpatterns = [
    path('', views.tmtext, name='main'),
    path('series/<int:pk>', views.tmlist, name='tmlist'),
    path('it_sounds_good/<int:tmt_id>',views.it_sounds_good, name='it_sounds_good'),
    path('subscribe/<int:series>',views.subscribe, name='subscribe'),
    path('tmtext/<int:tmt_id>',views.tmtext_detail, name='tmtext_detail'),
]