from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Gestión de usuarios (solo admins)
    path('gestion/', views.gestion_usuarios, name='gestion_usuarios'),
    path('lista/', views.lista_usuarios, name='users_lista'),

    # Registro de nuevos usuarios
    path('registro/', views.registro, name='registro'),

    # Perfil
    path('perfil/', views.perfil_usuario, name='perfil_usuario'),
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),

    # Logout
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
]
