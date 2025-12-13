from django.shortcuts import (
    get_object_or_404,
    redirect,
    render
)

from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q

from apps.blog.forms import (
    ArticuloForm,
    RegistroForm,
    PerfilForm,
    ComentarioForm,
    CategoriaForm,
    EditarPerfilForm,
    CambiarPasswordForm
)

from .models import (
    Articulo,
    Categoria,
    Comentario,
    Perfil
)

from .forms import ContactoForm
from django.db.models import Count

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

    # Obtener categorías populares ordenadas por cantidad de artículos y comentarios
    categorias_populares = Categoria.objects.annotate(
        total_articulos=Count('articulos', distinct=True),
        total_comentarios=Count('articulos__comentarios', distinct=True),
    ).filter(total_articulos__gt=0).order_by('-total_articulos', '-total_comentarios')[:8]

    context = {
        'destacados': articulos_destacados,
        'noticias': ultimas_noticias,
        'orden_actual': orden,
        'categorias': categorias_populares,
    }
    return render(request, 'pages/index.html', context)


def listar_por_categoria(request, categoria_id):
    """Vista para mostrar artículos filtrados por categoría"""
    categoria = get_object_or_404(Categoria, id=categoria_id)
    orden = request.GET.get('orden', 'reciente')
    
    orden_opciones = {
        'reciente': '-fecha_creacion',
        'antigua': 'fecha_creacion',
        'alpha_asc': 'titulo',
        'alpha_desc': '-titulo'
    }
    campo_orden = orden_opciones.get(orden, '-fecha_creacion')
    
    # Filtrar artículos por categoría
    articulos_destacados = Articulo.objects.filter(
        categoria=categoria, 
        destacado=True
    ).order_by('-fecha_creacion')[:3]
    
    noticias = Articulo.objects.filter(categoria=categoria).order_by(campo_orden)
    
    # Obtener categorías populares
    categorias_populares = Categoria.objects.annotate(
        total_articulos=Count('articulos', distinct=True),
        total_comentarios=Count('articulos__comentarios', distinct=True),
    ).filter(total_articulos__gt=0).order_by('-total_articulos', '-total_comentarios')[:8]
    
    context = {
        'destacados': articulos_destacados,
        'noticias': noticias,
        'orden_actual': orden,
        'categorias': categorias_populares,
        'categoria_seleccionada': categoria,
    }
    return render(request, 'pages/index.html', context)

def about(request):
    return render(request, 'pages/about.html')

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
    return render(request, 'register.html', {'form': form})

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

@login_required
def editar_articulo(request, id):
    articulo = get_object_or_404(Articulo, id=id)
    
    # Verificar permisos: admin puede editar todo, colaborador solo sus artículos
    es_admin = request.user.is_superuser or (hasattr(request.user, 'perfil') and request.user.perfil.es_administrador())
    es_autor = request.user == articulo.autor
    
    if not (es_admin or es_autor):
        messages.error(request, 'No tienes permiso para editar este artículo.')
        return redirect('detalle_articulo', id=id)
    
    if request.method == 'POST':
        form = ArticuloForm(request.POST, request.FILES, instance=articulo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Artículo actualizado exitosamente.')
            return redirect('detalle_articulo', id=articulo.id)
    else:
        form = ArticuloForm(instance=articulo)
    return render(request, 'blog/articulo_form.html', {'form': form, 'titulo': 'Editar Artículo'})

@login_required
def eliminar_articulo(request, id):
    articulo = get_object_or_404(Articulo, id=id)
    
    # Verificar permisos: admin puede eliminar todo, colaborador solo sus artículos
    es_admin = request.user.is_superuser or (hasattr(request.user, 'perfil') and request.user.perfil.es_administrador())
    es_autor = request.user == articulo.autor
    
    if not (es_admin or es_autor):
        messages.error(request, 'No tienes permiso para eliminar este artículo.')
        return redirect('detalle_articulo', id=id)
    
    if request.method == 'POST':
        articulo.delete()
        messages.success(request, 'Artículo eliminado exitosamente.')
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

def terms(request):
    """Vista para mostrar términos y condiciones"""
    return render(request, 'terms.html')

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
    # Obtener parámetro de búsqueda
    busqueda = request.GET.get('buscar', '').strip()
    
    # Filtrar usuarios
    usuarios = User.objects.all().select_related('perfil').order_by('username')
    
    if busqueda:
        usuarios = usuarios.filter(
            Q(username__icontains=busqueda) | 
            Q(email__icontains=busqueda) |
            Q(first_name__icontains=busqueda) |
            Q(last_name__icontains=busqueda)
        )
    
    # Verificar si el usuario actual es superusuario
    es_superusuario = request.user.is_superuser
    
    if request.method == 'POST':
        usuario_id = request.POST.get('usuario_id')
        nuevo_rol = request.POST.get('rol')
        
        if usuario_id and nuevo_rol:
            try:
                usuario = User.objects.get(id=usuario_id)
                perfil, created = Perfil.objects.get_or_create(usuario=usuario)
                
                # No permitir cambiar el rol de superusuarios
                if usuario.is_superuser:
                    messages.warning(request, 'No se puede modificar el rol de un superusuario')
                # No permitir que administradores cambien roles de otros administradores
                elif perfil.rol == 'administrador' and not es_superusuario:
                    messages.error(request, 'Solo el superusuario puede modificar roles de administradores')
                # Solo superusuarios pueden asignar rol de administrador
                elif nuevo_rol == 'administrador' and not es_superusuario:
                    messages.error(request, 'Solo el superusuario puede asignar el rol de administrador')
                # Validar que el rol sea válido
                elif nuevo_rol in ['miembro', 'colaborador', 'administrador']:
                    perfil.rol = nuevo_rol
                    perfil.save()
                    # Mensaje eliminado - ya se muestra en el frontend con JavaScript
                else:
                    messages.error(request, 'Rol no válido')
                    
            except User.DoesNotExist:
                messages.error(request, 'Usuario no encontrado')
        
        return redirect('gestion_usuarios')
    
    # Roles disponibles según el tipo de usuario
    if es_superusuario:
        roles_disponibles = [
            ('miembro', 'Miembro'), 
            ('colaborador', 'Colaborador'),
            ('administrador', 'Administrador')
        ]
    else:
        roles_disponibles = [('miembro', 'Miembro'), ('colaborador', 'Colaborador')]
    
    context = {
        'usuarios': usuarios,
        'roles_disponibles': roles_disponibles,
        'busqueda': busqueda,
        'es_superusuario': es_superusuario,
    }
    return render(request, 'admin/gestion_usuarios.html', context)


# ========== GESTIÓN DE CATEGORÍAS (ADMIN) ==========
@user_passes_test(es_administrador, login_url='index')
def crear_categoria(request):
    """Vista para crear una nueva categoría (solo administradores)"""
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría creada exitosamente')
            return redirect('gestion_categorias')
    else:
        form = CategoriaForm()
    
    return render(request, 'admin/categoria_form.html', {'form': form, 'accion': 'Crear'})

@user_passes_test(es_administrador, login_url='index')
def editar_categoria(request, id):
    """Vista para editar una categoría existente (solo administradores)"""
    categoria = get_object_or_404(Categoria, id=id)
    
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría actualizada exitosamente')
            return redirect('gestion_categorias')
    else:
        form = CategoriaForm(instance=categoria)
    
    return render(request, 'admin/categoria_form.html', {'form': form, 'accion': 'Editar', 'categoria': categoria})

@user_passes_test(es_administrador, login_url='index')
def eliminar_categoria(request, id):
    """Vista para eliminar una categoría (solo administradores)"""
    categoria = get_object_or_404(Categoria, id=id)
    
    # Verificar si tiene artículos asociados
    if categoria.articulos.exists():
        messages.error(request, f'No se puede eliminar "{categoria.nombre}" porque tiene {categoria.articulos.count()} artículos asociados')
        return redirect('gestion_categorias')
    
    if request.method == 'POST':
        nombre = categoria.nombre
        categoria.delete()
        messages.success(request, f'Categoría "{nombre}" eliminada exitosamente')
        return redirect('gestion_categorias')
    
    return render(request, 'admin/categoria_confirm_delete.html', {'categoria': categoria})

@user_passes_test(es_administrador, login_url='index')
def gestion_categorias(request):
    """Vista para listar y gestionar todas las categorías (solo administradores)"""
    categorias = Categoria.objects.all().order_by('nombre')
    
    # Agregar conteo de artículos por categoría
    for categoria in categorias:
        categoria.total_articulos = categoria.articulos.count()
    
    return render(request, 'admin/gestion_categorias.html', {'categorias': categorias})

@login_required
def editar_perfil(request):
    """Vista para editar el perfil del usuario"""
    if request.method == 'POST':
        form_perfil = EditarPerfilForm(request.POST, instance=request.user)
        form_password = CambiarPasswordForm(request.user, request.POST)
        
        # Determinar qué formulario se envió
        if 'guardar_perfil' in request.POST:
            if form_perfil.is_valid():
                form_perfil.save()
                messages.success(request, 'Perfil actualizado exitosamente.')
                return redirect('editar_perfil')
        elif 'cambiar_password' in request.POST:
            if form_password.is_valid():
                user = form_password.save()
                update_session_auth_hash(request, user)  # Mantener la sesión activa
                messages.success(request, 'Contraseña cambiada exitosamente.')
                return redirect('editar_perfil')
    else:
        form_perfil = EditarPerfilForm(instance=request.user)
        form_password = CambiarPasswordForm(request.user)
    
    context = {
        'form_perfil': form_perfil,
        'form_password': form_password,
    }
    return render(request, 'users/editar_perfil.html', context)


# ================================================
# VISTAS DE GESTIÓN DE USUARIOS (movidas desde users app)
# ================================================

from .decorators import administrador_required, visitante_required

# Roles disponibles
ROLES_DISPONIBLES = [
    ('miembro', 'Miembro'),
    ('colaborador', 'Colaborador'),
    ('administrador', 'Administrador'),
]

@administrador_required
def gestion_usuarios(request):
    if request.method == 'POST':
        usuario_id = request.POST.get('usuario_id')
        nuevo_rol = request.POST.get('rol')

        try:
            usuario = User.objects.get(id=usuario_id)
            if not usuario.is_superuser:
                perfil = Perfil.objects.get_or_create(user=usuario)[0]
                perfil.rol = nuevo_rol
                perfil.save()
            else:
                messages.error(request, 'No se puede modificar el rol del superusuario.')
        except User.DoesNotExist:
            messages.error(request, 'Usuario no encontrado.')

        return redirect('gestion_usuarios')

    # Asegurar que todos tengan perfil
    for u in User.objects.all():
        Perfil.objects.get_or_create(user=u)

    usuarios = User.objects.all()
    return render(request, 'admin/gestion_usuarios.html', {
        'usuarios': usuarios,
        'roles_disponibles': ROLES_DISPONIBLES,
        'es_superusuario': request.user.is_superuser
    })


@administrador_required
def lista_usuarios(request):
    usuarios = User.objects.all()
    return render(request, 'users/lista_usuarios.html', {
        'usuarios': usuarios
    })


@login_required
def perfil_usuario(request):
    usuario = request.user
    return render(request, 'users/perfil.html', {
        'usuario_perfil': usuario,
        'es_propio': True
    })


@login_required
def editar_perfil_usuario(request):
    if request.method == 'POST':
        form = PerfilForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil actualizado correctamente.")
            return redirect('perfil_usuario')
    else:
        form = PerfilForm(instance=request.user)
    
    return render(request, 'users/editar_perfil.html', {'form': form})


@login_required
def cambiar_password(request):
    from django.contrib.auth.forms import PasswordChangeForm
    
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Contraseña actualizada correctamente.")
            return redirect('perfil_usuario')
    else:
        form = PasswordChangeForm(request.user)
    
    for field in form.fields.values():
        field.widget.attrs['class'] = 'form-control'
    
    return render(request, 'users/cambiar_password.html', {
        'form': form,
        'titulo': 'Cambiar Contraseña'
    })
