from django.shortcuts import (
    get_object_or_404,
    render
)

from .models import (
    Articulo,
    Categoria
)

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

def detalle_articulo(request, id):
    # Busca el artículo o devuelve error 404 si no existe
    articulo = get_object_or_404(Articulo, id=id)
    
    # Opcional: Traer comentarios relacionados (si ya quieres prepararlo)
    comentarios = articulo.comentarios.all()

    context = {
        'articulo': articulo,
        'comentarios': comentarios,
    }
    return render(request, 'blog/articulo_detail.html', context)