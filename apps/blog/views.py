from django.shortcuts import (
    get_object_or_404,
    redirect,
    render
)

from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User
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

from .forms import ContactoForm

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

@login_required
def editar_comentario(request, id):
    comentario = get_object_or_404(Comentario, id=id)
    
    # Lógica de Permisos: ¿Es autor O es colaborador/admin?
    es_autor = request.user == comentario.autor
    es_colaborador = request.user.is_superuser or (hasattr(request.user, 'perfil') and request.user.perfil.rol == 'colaborador')

    # Si NO tiene ninguno de los dos permisos, lo sacamos
    if not es_autor and not es_colaborador:
        return redirect('detalle_articulo', id=comentario.articulo.id)

    if request.method == 'POST':
        form = ComentarioForm(request.POST, instance=comentario)
        if form.is_valid():
            form.save()
            return redirect('detalle_articulo', id=comentario.articulo.id)
    else:
        form = ComentarioForm(instance=comentario)

    # Pasamos una variable extra al template para saber que título poner
    titulo = "Editar Comentario" if es_autor else f"Moderando comentario de {comentario.autor.username}"
    
    return render(request, 'blog/comentario_form.html', {
        'form': form, 
        'comentario': comentario,
        'titulo_pagina': titulo 
    })

@login_required
def eliminar_comentario(request, id):
    comentario = get_object_or_404(Comentario, id=id)
    
    # Misma lógica de permisos
    es_autor = request.user == comentario.autor
    es_colaborador = request.user.is_superuser or (hasattr(request.user, 'perfil') and request.user.perfil.rol == 'colaborador')

    if not es_autor and not es_colaborador:
        return redirect('detalle_articulo', id=comentario.articulo.id)
    
    if request.method == 'POST':
        articulo_id = comentario.articulo.id
        comentario.delete()
        return redirect('detalle_articulo', id=articulo_id)
    
    return render(request, 'blog/comentario_confirm_delete.html', {'comentario': comentario})

def contact(request):
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            # 1. Guardar el mensaje en la Base de Datos
            mensaje_nuevo = form.save()
            
            # 2. Preparar el correo
            asunto = f'Nuevo mensaje de contacto de {mensaje_nuevo.nombre}'
            cuerpo_mensaje = f"""
            Has recibido un nuevo mensaje desde TodoDeporte:
            
            Nombre: {mensaje_nuevo.nombre}
            Email: {mensaje_nuevo.email}
            Mensaje: 
            {mensaje_nuevo.mensaje}
            """
            
            # Obtener emails de todos los superusuarios
            emails_admins = User.objects.filter(is_superuser=True).values_list('email', flat=True)
            
            # 3. Enviar el correo
            try:
                send_mail(
                    asunto,
                    cuerpo_mensaje,
                    settings.EMAIL_HOST_USER if hasattr(settings, 'EMAIL_HOST_USER') else 'noreply@tododeporte.com',
                    list(emails_admins), # Lista de destinatarios
                    fail_silently=False,
                )
                messages.success(request, '¡Tu mensaje ha sido enviado correctamente!')
                return redirect('contact') # Redirigir a la misma página para limpiar el form
            except Exception as e:
                messages.error(request, 'Ocurrió un error al enviar el correo. Inténtalo más tarde.')
                
    else:
        form = ContactoForm()

    return render(request, 'pages/contact.html', {'form': form})

def listar_por_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    # Filtramos los artículos que pertenecen a esta categoría
    noticias = Articulo.objects.filter(categoria=categoria).order_by('-fecha_creacion')
    
    context = {
        'noticias': noticias,
        'categoria_seleccionada': categoria,
        # Nota: No necesitamos pasar 'categorias' aquí, porque el context_processor ya lo hace globalmente
    }
    # Reutilizamos el template index.html o index.html (ahora pages/index.html) para mostrar la lista
    return render(request, 'pages/index.html', context)
