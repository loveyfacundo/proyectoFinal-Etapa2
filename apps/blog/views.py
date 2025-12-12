from django.shortcuts import get_object_or_404, redirect, render
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count

from apps.blog.forms import (
    ArticuloForm,
    RegistroForm,
    ComentarioForm,
    EditarPerfilForm,
    CambiarPasswordForm
)

from .models import (
    Articulo,
    Categoria,
    Comentario,
    Perfil,
    AcercaDe
)

from .forms import ContactoForm


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
    return user.is_authenticated and (user.is_superuser or (hasattr(user, 'perfil') and user.perfil.es_colaborador_o_superior()))


# --- Verifica si es administrador ---
def es_administrador(user):
    return user.is_authenticated and (user.is_superuser or (hasattr(user, 'perfil') and user.perfil.es_administrador()))


@user_passes_test(es_colaborador)
def crear_articulo(request):
    if request.method == 'POST':
        form = ArticuloForm(request.POST, request.FILES)
        if form.is_valid():
            articulo = form.save(commit=False)
            articulo.autor = request.user
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
    es_autor = request.user == comentario.autor
    es_colaborador = request.user.is_superuser or (hasattr(request.user, 'perfil') and request.user.perfil.es_colaborador_o_superior())
    if not es_autor and not es_colaborador:
        return redirect('detalle_articulo', id=comentario.articulo.id)

    if request.method == 'POST':
        form = ComentarioForm(request.POST, instance=comentario)
        if form.is_valid():
            form.save()
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
    es_colaborador = request.user.is_superuser or (hasattr(request.user, 'perfil') and request.user.perfil.es_colaborador_o_superior())

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
            mensaje_nuevo = form.save()

            asunto = f'Nuevo mensaje de contacto de {mensaje_nuevo.nombre}'
            cuerpo_mensaje = f"""
            Has recibido un nuevo mensaje desde TodoDeporte:
            
            Nombre: {mensaje_nuevo.nombre}
            Email: {mensaje_nuevo.email}
            Mensaje: 
            {mensaje_nuevo.mensaje}
            """
            
            emails_admins = User.objects.filter(is_superuser=True).values_list('email', flat=True)

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
    """Vista para que administradores gestionen roles de usuarios"""
    usuarios = User.objects.all().select_related('perfil').order_by('username')
    
    if request.method == 'POST':
        usuario_id = request.POST.get('usuario_id')
        nuevo_rol = request.POST.get('rol')
        
        if usuario_id and nuevo_rol:
            try:
                usuario = User.objects.get(id=usuario_id)
                # No permitir cambiar el rol de superusuarios
                if not usuario.is_superuser:
                    perfil, created = Perfil.objects.get_or_create(usuario=usuario)
                    # Administradores solo pueden asignar roles de miembro o colaborador
                    if nuevo_rol in ['miembro', 'colaborador']:
                        perfil.rol = nuevo_rol
                        perfil.save()
                        messages.success(request, f'Rol de {usuario.username} actualizado a {perfil.get_rol_display()}')
                    else:
                        messages.error(request, 'No tienes permisos para asignar ese rol')
                else:
                    messages.warning(request, 'No se puede modificar el rol de un superusuario')
            except User.DoesNotExist:
                messages.error(request, 'Usuario no encontrado')
        
        return redirect('gestion_usuarios')
    
    # Solo roles que el administrador puede asignar
    roles_disponibles = [('miembro', 'Miembro'), ('colaborador', 'Colaborador')]
    
    context = {
        'usuarios': usuarios,
        'roles_disponibles': roles_disponibles,
    }
    return render(request, 'users/gestion_usuarios.html', context)


@login_required
def perfil_usuario(request, username=None):
    """Vista para mostrar el perfil de un usuario"""
    if username:
        # Ver perfil de otro usuario
        usuario = get_object_or_404(User, username=username)
        es_propio = request.user == usuario
    else:
        # Ver perfil propio
        usuario = request.user
        es_propio = True
    
    # Obtener estadísticas
    total_articulos = usuario.articulos.count() if hasattr(usuario, 'articulos') else 0
    total_comentarios = usuario.comentarios.count() if hasattr(usuario, 'comentarios') else 0
    
    # Obtener artículos del usuario (si es colaborador o superior)
    articulos = []
    if hasattr(usuario, 'perfil') and usuario.perfil.es_colaborador_o_superior():
        articulos = usuario.articulos.order_by('-fecha_creacion')[:10]
    
    context = {
        'usuario_perfil': usuario,
        'es_propio': es_propio,
        'total_articulos': total_articulos,
        'total_comentarios': total_comentarios,
        'articulos': articulos,
    }
    
    return render(request, 'users/perfil.html', context)


@login_required
def editar_perfil(request):
    """Vista para editar el perfil del usuario"""
    if request.method == 'POST':
        form = EditarPerfilForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Tu perfil ha sido actualizado correctamente.')
            return redirect('perfil_usuario')
    else:
        form = EditarPerfilForm(instance=request.user)
    
    context = {
        'form': form,
        'titulo': 'Editar Perfil'
    }
    return render(request, 'users/editar_perfil.html', context)


@login_required
def cambiar_password(request):
    """Vista para cambiar la contraseña"""
    if request.method == 'POST':
        form = CambiarPasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Actualizar la sesión para que no se desloguee
            update_session_auth_hash(request, user)
            messages.success(request, '🔒 Tu contraseña ha sido cambiada exitosamente.')
            return redirect('perfil_usuario')
        else:
            messages.error(request, '❌ Por favor corrige los errores.')
    else:
        form = CambiarPasswordForm(request.user)
    
    context = {
        'form': form,
        'titulo': 'Cambiar Contraseña'
    }
    return render(request, 'users/cambiar_password.html', context)