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
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count

from apps.blog.forms import (
    ArticuloForm,
    RegistroForm,
    ComentarioForm
)

from .models import (
    Articulo,
    Categoria,
    Comentario,
    Perfil
)

from .forms import ContactoForm
from .models import AcercaDe


def index(request):
    orden = request.GET.get('orden', 'reciente')
    
    orden_opciones = {
        'reciente': '-fecha_creacion',
        'antigua': 'fecha_creacion',
        'alpha_asc': 'titulo',
        'alpha_desc': '-titulo'
    }
    campo_orden = orden_opciones.get(orden, '-fecha_creacion')

    articulos_destacados = Articulo.objects.filter(destacado=True).order_by('-fecha_creacion')[:3]
    
    if orden == 'reciente':
        ultimas_noticias = Articulo.objects.order_by(campo_orden)[:6]
    else:
        ultimas_noticias = Articulo.objects.order_by(campo_orden)

    context = {
        'destacados': articulos_destacados,
        'noticias': ultimas_noticias,
        'orden_actual': orden, # Pasamos esto para que el select recuerde la opción
    }
    return render(request, 'pages/index.html', context)


def about(request):
    try:
        acerca_de = AcercaDe.objects.first()
        
        # Si existe contenido de integrantes, procesarlo
        if acerca_de and acerca_de.integrantes:
            # Procesar cada línea para destacar el nombre
            lineas_procesadas = []
            for linea in acerca_de.integrantes.split('\n'):
                linea = linea.strip()
                if linea and '-' in linea:
                    # Formato: "• Nombre Apellido - Cargo"
                    # Separar nombre y cargo
                    partes = linea.split(' - ', 1)
                    if len(partes) == 2:
                        nombre = partes[0].replace('•', '').strip()
                        cargo = partes[1].strip()
                        # Crear HTML con nombre en negrita
                        linea_formateada = f"<strong>{nombre}</strong> - {cargo}"
                        lineas_procesadas.append(linea_formateada)
                    else:
                        lineas_procesadas.append(linea)
                elif linea:
                    lineas_procesadas.append(linea)
            
            # Unir las líneas procesadas
            integrantes_html = '\n'.join(lineas_procesadas)
        else:
            integrantes_html = None
            
    except:
        acerca_de = None
        integrantes_html = None
    
    context = {
        'acerca_de': acerca_de,
        'integrantes_html': integrantes_html
    }
    return render(request, 'pages/about.html', context)


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


def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            return redirect('index') # Redirigir al inicio
    else:
        form = RegistroForm()
    return render(request, 'users/register.html', {'form': form})


# --- Verifica si es superusuario O si tiene el rol de colaborador o administrador ---
def es_colaborador(user):
    return user.is_authenticated and (
        user.is_superuser or (
            hasattr(user, 'perfil_users') and
            user.perfil_users.es_colaborador_o_superior()
        )
    )

def es_administrador(user):
    return user.is_authenticated and (
        user.is_superuser or (
            hasattr(user, 'perfil_users') and
            user.perfil_users.es_administrador()
        )
    )

# --- ARTÍCULOS ---
@user_passes_test(es_colaborador)
def crear_articulo(request):
    if request.method == 'POST':
        form = ArticuloForm(request.POST, request.FILES)
        if form.is_valid():
            articulo = form.save(commit=False)
            articulo.autor = request.user
            articulo.save()
            messages.success(request, "Artículo creado correctamente.")
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
            messages.success(request, "Artículo editado correctamente.")
            return redirect('detalle_articulo', id=articulo.id)
    else:
        form = ArticuloForm(instance=articulo)
    return render(request, 'blog/articulo_form.html', {'form': form, 'titulo': 'Editar Artículo'})

@user_passes_test(es_colaborador)
def eliminar_articulo(request, id):
    articulo = get_object_or_404(Articulo, id=id)
    if request.method == 'POST':
        articulo.delete()
        messages.success(request, "Artículo eliminado correctamente.")
        return redirect('index')
    return render(request, 'blog/articulo_confirm_delete.html', {'articulo': articulo})
def detalle_articulo(request, id):
    articulo = get_object_or_404(Articulo, id=id)
    comentarios = Comentario.objects.filter(articulo=articulo).order_by('-id')

    if request.method == 'POST' and request.user.is_authenticated:
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.autor = request.user
            comentario.articulo = articulo
            comentario.save()
            messages.success(request, "Comentario publicado.")
            return redirect('detalle_articulo', id=id)
    else:
        form = ComentarioForm()

    return render(request, 'blog/detalle_articulo.html', {
        'articulo': articulo,
        'comentarios': comentarios,
        'form': form
    })

# --- COMENTARIOS ---
@login_required
def editar_comentario(request, id):
    comentario = get_object_or_404(Comentario, id=id)
    es_autor = request.user == comentario.autor
    es_colaborador_user = (
        request.user.is_superuser or
        (hasattr(request.user, 'perfil_users') and request.user.perfil_users.es_colaborador_o_superior())
    )

    if not es_autor and not es_colaborador_user:
        messages.error(request, "No tienes permiso para editar este comentario.")
        return redirect('detalle_articulo', id=comentario.articulo.id)

    if request.method == 'POST':
        form = ComentarioForm(request.POST, instance=comentario)
        if form.is_valid():
            form.save()
            messages.success(request, "Comentario actualizado correctamente.")
            return redirect('detalle_articulo', id=comentario.articulo.id)
    else:
        form = ComentarioForm(instance=comentario)

    titulo = "Editar Comentario" if es_autor else f"Moderando comentario de {comentario.autor.username}"
    return render(request, 'blog/comentario_form.html', {
        'form': form,
        'comentario': comentario,
        'titulo_pagina': titulo
    })

@login_required
def eliminar_comentario(request, id):
    comentario = get_object_or_404(Comentario, id=id)
    es_autor = request.user == comentario.autor
    es_colaborador_user = (
        request.user.is_superuser or
        (hasattr(request.user, 'perfil_users') and request.user.perfil_users.es_colaborador_o_superior())
    )

    if not es_autor and not es_colaborador_user:
        messages.error(request, "No tienes permiso para eliminar este comentario.")
        return redirect('detalle_articulo', id=comentario.articulo.id)

    if request.method == 'POST':
        articulo_id = comentario.articulo.id
        comentario.delete()
        messages.success(request, "Comentario eliminado correctamente.")
        return redirect('detalle_articulo', id=articulo_id)

    return render(request, 'blog/comentario_confirm_delete.html', {'comentario': comentario})
def about(request):
    return render(request, 'blog/about.html')
def contact(request):
    return render(request, 'blog/contact.html')
def listar_por_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    orden = request.GET.get('orden', 'reciente')
    
    orden_opciones = {
        'reciente': '-fecha_creacion',
        'antigua': 'fecha_creacion',
        'alpha_asc': 'titulo',
        'alpha_desc': '-titulo'
    }
    campo_orden = orden_opciones.get(orden, '-fecha_creacion')
    
    noticias = Articulo.objects.filter(categoria=categoria).order_by(campo_orden)
    
    context = {
        'noticias': noticias,
        'categoria_seleccionada': categoria,
        'orden_actual': orden,
    }
    return render(request, 'pages/index.html', context)


@user_passes_test(es_administrador)
def gestion_usuarios(request):
    usuarios = User.objects.all().order_by('username')
    perfiles = Perfil.objects.all()

    return render(request, 'blog/gestion_usuarios.html', {
        'usuarios': usuarios,
        'roles_disponibles': roles_disponibles,
    }
    return render(request, 'users/gestion_usuarios.html', context)