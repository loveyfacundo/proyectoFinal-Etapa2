from django.urls import path
from django.contrib.auth import views as auth_views 
from . import views

urlpatterns = [
    # PÁGINAS PRINCIPALES
    path('', views.index, name='index'),
    path('nosotros/', views.about, name='about'),
    path('contacto/', views.contact, name='contact'),

    # GESTIÓN DE ARTÍCULOS
    path('articulo/<int:id>/', views.detalle_articulo, name='detalle_articulo'),
    path('crear/', views.crear_articulo, name='crear_articulo'),
    path('editar/<int:id>/', views.editar_articulo, name='editar_articulo'),
    path('eliminar/<int:id>/', views.eliminar_articulo, name='eliminar_articulo'),

    # GESTIÓN DE COMENTARIOS
    path('comentario/editar/<int:id>/', views.editar_comentario, name='editar_comentario'),
    path('comentario/eliminar/<int:id>/', views.eliminar_comentario, name='eliminar_comentario'),

    # GESTIÓN DE CATEGORÍAS
    path('categoria/<int:categoria_id>/', views.listar_por_categoria, name='listar_por_categoria'),

    # GESTIÓN DE USUARIOS (ADMIN)
    path('admin/usuarios/', views.gestion_usuarios, name='gestion_usuarios'),

    # RUTAS DE AUTENTICACIÓN
    path('registro/', views.registro, name='registro'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
]

