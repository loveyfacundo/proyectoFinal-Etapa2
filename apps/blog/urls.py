from django.urls import path
from django.contrib.auth import views as auth_views # Importamos vistas de auth
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('nosotros/', views.about, name='about'),
    path('contacto/', views.contact, name='contact'),

    # URL para poder ver detalle de un artículo
    path('articulo/<int:id>/', views.detalle_articulo, name='detalle_articulo'),

    # Rutas para Comentarios
    path('comentario/editar/<int:id>/', views.editar_comentario, name='editar_comentario'),
    path('comentario/eliminar/<int:id>/', views.eliminar_comentario, name='eliminar_comentario'),

    # GESTIÓN DE ARTÍCULOS (Solo Colaboradores)
    path('crear/', views.crear_articulo, name='crear_articulo'),
    path('editar/<int:id>/', views.editar_articulo, name='editar_articulo'),
    path('eliminar/<int:id>/', views.eliminar_articulo, name='eliminar_articulo'),

    # Rutas para Categorías
    path('categoria/<int:categoria_id>/', views.listar_por_categoria, name='listar_por_categoria'),

    # RUTAS DE AUTENTICACIÓN
    path('registro/', views.registro, name='registro'),
    
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    
    # Logout: Django 5 requiere que el logout sea por POST o usar un paso intermedio. 
    # Para simplificar, usamos la vista genérica que redirige tras cerrar sesión.
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
]
