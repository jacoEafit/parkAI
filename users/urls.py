from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('vehicleManagement/', views.vehicleManagement, name='vehicleManagement'),
    path('login/', views.login_view, name='login'),
    path('register', views.register, name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('userManagement/', views.userManagement)
]