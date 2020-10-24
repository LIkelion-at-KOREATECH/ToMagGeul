from django.urls import path
from user import views

urlpatterns = [
    path('register/', views.signup, name='user_register'),
    path('register/author', views.createauthor, name='author_register'),
    path('thank/', views.thankyou, name='thank'),
    path('signin/',views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('profile/<str:author>', views.profile, name='profile'),
    path('mypage/', views.mypage, name='mypage'),
]