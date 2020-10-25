from django.urls import path
from tomaggeultext import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.tmtext, name='main'),
    path('create/', views.tmtextcreate, name='create'),
    path('tmlist', views.tmlist, name='tmlist'),
    path('createseries/',views.tmseriescreate, name='createseries'),
    path('series/<int:pk>', views.tmlist, name='tmlist'),
    path('series/<int:pk>', views.tmlist, name='series'),
    path('it_sounds_good/<int:tmt_id>',views.it_sounds_good, name='it_sounds_good'),
    path('subscribe/<int:series>',views.subscribe, name='subscribe'),
    path('tmtext/<int:tmt_id>',views.tmtext_detail, name='tmtext_detail'),
    path('popup/',views.popup, name='popup'),
] + static(settings.MEDIA_URL,
document_root=settings.MEDIA_ROOT)