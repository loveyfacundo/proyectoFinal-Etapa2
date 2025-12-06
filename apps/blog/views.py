from django.shortcuts import (
    get_object_or_404,
    redirect,
    render
)

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test

from apps.blog.forms import (
    ArticuloForm,
    RegistroForm,
    ComentarioForm
)

from .models import (
    Articulo,
    Categoria,
    Comentario
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
    articulo = get_object_or_404(Articulo, id=id)
    comentarios = articulo.comentarios.all().order_by('-fecha_creacion')
    form = ComentarioForm()

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = ComentarioForm(request.POST)
            if form.is_valid():
                comentario = form.save(commit=False)
                comentario.articulo = articulo
                comentario.autor = request.user
                comentario.save()
                return redirect('detalle_articulo', id=id)
        else:
            return redirect('login')

    context = {
        'articulo': articulo,
        'comentarios': comentarios,
        'form': form,
    }
    return render(request, 'blog/articulo_detail.html', context)

@login_required
def editar_comentario(request, id):
    comentario = get_object_or_404(Comentario, id=id)
    
    # Seguridad: Solo el autor puede editar
    if request.user != comentario.autor:
        return redirect('detalle_articulo', id=comentario.articulo.id)

    if request.method == 'POST':
        form = ComentarioForm(request.POST, instance=comentario)
        if form.is_valid():
            form.save()
            return redirect('detalle_articulo', id=comentario.articulo.id)
    else:
        form = ComentarioForm(instance=comentario)

    return render(request, 'blog/comentario_form.html', {
        'form': form, 
        'comentario': comentario
    })




def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            # Loguear al usuario inmediatamente después de registrarse
            login(request, usuario)
            return redirect('index') # Redirigir al inicio
    else:
        form = RegistroForm()
    
    return render(request, 'users/register.html', {'form': form})

@login_required
def eliminar_comentario(request, id):
    comentario = get_object_or_404(Comentario, id=id)
    
    # Seguridad: Solo el autor puede eliminar
    if request.user != comentario.autor:
        return redirect('detalle_articulo', id=comentario.articulo.id)
    
    if request.method == 'POST':
        articulo_id = comentario.articulo.id
        comentario.delete()
        return redirect('detalle_articulo', id=articulo_id)
    
    return render(request, 'blog/comentario_confirm_delete.html', {'comentario': comentario})

# --- FUNCIONES DE SEGURIDAD ---
def es_colaborador(user):
    # Verifica si es superusuario O si tiene el rol de colaborador en su perfil
    return user.is_authenticated and (user.is_superuser or (hasattr(user, 'perfil') and user.perfil.rol == 'colaborador'))

# --- VISTAS CRUD ARTÍCULOS ---

@user_passes_test(es_colaborador) # Solo entra si pasa la prueba
def crear_articulo(request):
    if request.method == 'POST':
        # Importante: request.FILES es necesario para subir imágenes
        form = ArticuloForm(request.POST, request.FILES)
        if form.is_valid():
            articulo = form.save(commit=False)
            articulo.autor = request.user # Asignamos el autor automáticamente
            articulo.save()
            return redirect('detalle_articulo', id=articulo.id)
    else:
        form = ArticuloForm()
    
    return render(request, 'blog/articulo_form.html', {'form': form, 'titulo': 'Crear Nuevo Artículo'})

@user_passes_test(es_colaborador)
def editar_articulo(request, id):
    articulo = get_object_or_404(Articulo, id=id)
    
    if request.method == 'POST':
        form = ArticuloForm(request.POST, request.FILES, instance=articulo)
        if form.is_valid():
            form.save()
            return redirect('detalle_articulo', id=articulo.id)
    else:
        form = ArticuloForm(instance=articulo)
    
    return render(request, 'blog/articulo_form.html', {'form': form, 'titulo': 'Editar Artículo'})

@user_passes_test(es_colaborador)
def eliminar_articulo(request, id):
    articulo = get_object_or_404(Articulo, id=id)
    
    if request.method == 'POST':
        articulo.delete()
        return redirect('index')
    
    return render(request, 'blog/articulo_confirm_delete.html', {'articulo': articulo})