from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test

from .models import Articulo, Comentario, Perfil, Categoria
from .forms import ArticuloForm, ComentarioForm

# --- VISTA INDEX (NECESARIA PARA QUE NO HAYA ERROR) ---
def index(request):
    articulos = Articulo.objects.all().order_by('-id')
    categorias = Categoria.objects.all()
    return render(
        request,
        'blog/index.html',
        {'articulos': articulos, 'categorias': categorias}
    )

# --- Funciones para verificar permisos ---
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
    articulos = Articulo.objects.filter(categoria=categoria).order_by('-id')

    return render(request, 'blog/listar_por_categoria.html', {
        'categoria': categoria,
        'articulos': articulos
    })
from django.contrib.auth.models import User

@user_passes_test(es_administrador)
def gestion_usuarios(request):
    usuarios = User.objects.all().order_by('username')
    perfiles = Perfil.objects.all()

    return render(request, 'blog/gestion_usuarios.html', {
        'usuarios': usuarios,
        'perfiles': perfiles,
    })
