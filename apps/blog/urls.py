from django.urls import path
from django.contrib.auth import views as auth_views 
from . import views

urlpatterns = [
    # PÁGINAS PRINCIPALES
    path('', views.index, name='index'),
    path('nosotros/', views.about, name='about'),
    path('contacto/', views.contact, name='contact'),
    path('terminos/', views.terms, name='terms'),

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

    # GESTIÓN DE USUARIOS (ADMINISTRADOR)
    path('gestion/usuarios/', views.gestion_usuarios, name='gestion_usuarios'),
    
    # GESTIÓN DE CATEGORÍAS (ADMINISTRADOR)
    path('gestion/categorias/', views.gestion_categorias, name='gestion_categorias'),
    path('gestion/categoria/crear/', views.crear_categoria, name='crear_categoria'),
    path('gestion/categoria/editar/<int:id>/', views.editar_categoria, name='editar_categoria'),
    path('gestion/categoria/eliminar/<int:id>/', views.eliminar_categoria, name='eliminar_categoria'),

    # RUTAS DE AUTENTICACIÓN Y USUARIOS
    path('registro/', views.registro, name='registro'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    
    # PERFIL DE USUARIO
    path('perfil/', views.perfil_usuario, name='perfil_usuario'),
    path('perfil/editar/', views.editar_perfil_usuario, name='editar_perfil'),
    path('perfil/cambiar-password/', views.cambiar_password, name='cambiar_password'),
    
    # LISTA DE USUARIOS (ADMIN)
    path('users/lista/', views.lista_usuarios, name='users_lista'),
]

