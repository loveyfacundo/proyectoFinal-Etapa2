from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('gestion/', views.gestion_usuarios, name='gestion_usuarios'),
    path('lista/', views.lista_usuarios, name='users_lista'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),

]
