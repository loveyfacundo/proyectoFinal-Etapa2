from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required

# Solo administradores
def administrador_required(view_func):
    @login_required
    def wrapper(request, *args, **kwargs):
        # Permitir acceso a superusuarios
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        # Verificar si el usuario tiene perfil y es administrador
        if hasattr(request.user, 'perfil_users'):
            if request.user.perfil_users.rol == 'administrador':
                return view_func(request, *args, **kwargs)
        raise PermissionDenied
    return wrapper

# Solo colaboradores o administradores
def colaborador_required(view_func):
    @login_required
    def wrapper(request, *args, **kwargs):
        # Permitir acceso a superusuarios
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        # Verificar si el usuario tiene perfil y es colaborador o administrador
        if hasattr(request.user, 'perfil_users'):
            if request.user.perfil_users.rol in ['colaborador', 'administrador']:
                return view_func(request, *args, **kwargs)
        raise PermissionDenied
    return wrapper

# Solo miembros o superiores (miembro, colaborador o admin)
def miembro_required(view_func):
    @login_required
    def wrapper(request, *args, **kwargs):
        # Permitir acceso a superusuarios
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        # Verificar si el usuario tiene perfil y es miembro o superior
        if hasattr(request.user, 'perfil_users'):
            if request.user.perfil_users.rol in ['miembro', 'colaborador', 'administrador']:
                return view_func(request, *args, **kwargs)
        raise PermissionDenied
    return wrapper

# Visitantes — no requiere login
def visitante_required(view_func):
    def wrapper(request, *args, **kwargs):
        return view_func(request, *args, **kwargs)
    return wrapper
