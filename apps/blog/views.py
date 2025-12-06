from django.shortcuts import render
from .models import Articulo, Categoria

def index(request):
    # Traemos los artículos destacados para el carrusel
    articulos_destacados = Articulo.objects.filter(destacado=True).order_by('-fecha_creacion')[:3]
    
    # Traemos las últimas noticias (excluyendo los destacados si quisieras, o todos)
    ultimas_noticias = Articulo.objects.order_by('-fecha_creacion')[:6]
    
    # Traemos todas las categorías para el sidebar
    categorias = Categoria.objects.all()

    context = {
        'destacados': articulos_destacados,
        'noticias': ultimas_noticias,
        'categorias': categorias,
    }
    return render(request, 'pages/index.html', context)

# Vista para la página "Acerca de"
def about(request):
    return render(request, 'pages/about.html')

# Vista para la página "Contacto"
def contact(request):
    return render(request, 'pages/contact.html')

