from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Perfil
from .decorators import administrador_required, visitante_required

# Roles disponibles
ROLES_DISPONIBLES = [
    ('miembro', '👤 Miembro'),
    ('colaborador', '✏️ Colaborador'),
    ('administrador', '🔐 Administrador'),
]

# ----------------------
# Gestión de usuarios
# Solo administradores
# ----------------------
@administrador_required
def gestion_usuarios(request):
    if request.method == 'POST':
        usuario_id = request.POST.get('usuario_id')
        nuevo_rol = request.POST.get('rol')

        # DEBUG
        print("Usuario ID:", usuario_id, "Nuevo rol:", nuevo_rol)

        try:
            usuario = User.objects.get(id=usuario_id)
            if not usuario.is_superuser:
                perfil = Perfil.objects.get_or_create(user=usuario)[0]
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
    return render(request, 'users/gestion_usuarios.html', {
        'usuarios': usuarios,
        'roles_disponibles': ROLES_DISPONIBLES
    })



# ----------------------
# Lista de usuarios
# Solo administradores
# ----------------------
@administrador_required
def lista_usuarios(request):
    usuarios = User.objects.all()
    return render(request, 'users/lista_usuarios.html', {
        'usuarios': usuarios
    })


# ----------------------
# Registro de usuarios
# Visitantes
# ----------------------
@visitante_required
def registro(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password != password2:
            messages.error(request, "Las contraseñas no coinciden")
            return redirect('registro')

        if User.objects.filter(username=username).exists():
            messages.error(request, "El nombre de usuario ya existe")
            return redirect('registro')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, "Usuario registrado correctamente. Ya podés iniciar sesión.")
        return redirect('login')

    return render(request, 'users/registro.html')


# ----------------------
# Perfil de usuario
# Solo miembros o colaboradores
# ----------------------
@login_required
def perfil_usuario(request):
    usuario = request.user
    return render(request, 'users/perfil.html', {'usuario': usuario})

