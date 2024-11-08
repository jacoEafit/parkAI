from django.urls import path
from . import views

urlpatterns = [
    path('homeUsers', views.homeUsers, name='homeUsers'),
    path('guiarUsuario', views.guiarUsuario, name='guiarUsuario'),
    path('sobreNosotros', views.sobreNosotrosUsers, name='sobreNosotrosUsers'),
]