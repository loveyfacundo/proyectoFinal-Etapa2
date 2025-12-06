from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('nosotros/', views.about, name='about'),
    path('contacto/', views.contact, name='contact'),
]
