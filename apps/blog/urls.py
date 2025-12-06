from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('nosotros/', views.about, name='about'),
    path('contacto/', views.contact, name='contact'),

    # URL para poder ver detalle de un artículo
    path('articulo/<int:id>/', views.detalle_articulo, name='detalle_articulo'),
]
