from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from user import views

urlpatterns = [
    path('register/', views.signup, name='user_register'),
    path('register/author', views.createauthor, name='author_register'),
    path('thank/', views.thankyou, name='thank'),
    # path('signin/',LoginView.as_view(), name='signin'),
    path('signin/',views.MyLoginView.as_view(), name='signin'),
    path('logout/', LogoutView.as_view(), name='logout'),
]