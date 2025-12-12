from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import RegistroForm, PerfilForm
from .models import Perfil

# --- ROLES DISPONIBLES ---
ROLES_DISPONIBLES = [
    ('miembro', '👤 Miembro'),
    ('colaborador', '✏️ Colaborador'),
    ('administrador', '🔐 Administrador'),
]

# --- PERMISOS ---
def es_colaborador(user):
    return user.is_authenticated and (
        user.is_superuser or (
            hasattr(user, 'perfil_users') and
            user.perfil_users.rol in ['colaborador', 'administrador']
        )
    )

def es_administrador(user):
    return user.is_authenticated and (
        user.is_superuser or (
            hasattr(user, 'perfil_users') and
            user.perfil_users.rol == 'administrador'
        )
    )

# --- REGISTRO ---
def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            messages.success(request, "Usuario registrado correctamente.")
            return redirect('perfil_usuario')
    else:
        form = RegistroForm()
    return render(request, 'users/register.html', {'form': form})

# --- VER PERFIL ---
@login_required
def perfil_usuario(request):
    usuario = request.user
    return render(request, 'users/perfil.html', {'usuario': usuario})

# --- EDITAR PERFIL ---
@login_required
def editar_perfil(request):
    perfil = request.user.perfil_users
    if request.method == 'POST':
        form = PerfilForm(request.POST, request.FILES, instance=perfil, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil actualizado correctamente.")
            return redirect('perfil_usuario')
    else:
        form = PerfilForm(instance=perfil, user=request.user)

    return render(request, 'users/editar_perfil.html', {'form': form})

# --- GESTIÓN DE USUARIOS (solo para administradores) ---
@user_passes_test(es_administrador)
def gestion_usuarios(request):
    if request.method == 'POST':
        usuario_id = request.POST.get('usuario_id')
        nuevo_rol = request.POST.get('rol')
        try:
            usuario = User.objects.get(id=usuario_id)
            if not usuario.is_superuser:
                perfil, _ = Perfil.objects.get_or_create(user=usuario)
                perfil.rol = nuevo_rol
                perfil.save()
                messages.success(request, f'Rol de {usuario.username} actualizado a {nuevo_rol}.')
            else:
                messages.error(request, 'No se puede modificar el rol del superusuario.')
        except User.DoesNotExist:
            messages.error(request, 'Usuario no encontrado.')
        return redirect('gestion_usuarios')

    # Asegurar que todos tengan perfil
    for u in User.objects.all():
        Perfil.objects.get_or_create(user=u)

    usuarios = User.objects.all()
    return render(request, 'users/gestion_usuarios.html', {'usuarios': usuarios, 'roles_disponibles': ROLES_DISPONIBLES})


