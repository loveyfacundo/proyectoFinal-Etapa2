from .models import Categoria

def procesador_categorias(request):
    # devuelve un diccionario que estará disponible en TODOS los HTML
    return {
        'categorias_globales': Categoria.objects.all().order_by('nombre')
    }
