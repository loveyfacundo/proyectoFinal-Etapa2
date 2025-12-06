from django.shortcuts import render

# Vistas de páginas principales
def index(request):
    """Vista para la página de inicio"""
    return render(request, 'index.html')


def about(request):
    """Vista para la página Acerca de"""
    return render(request, 'about.html')


def contact(request):
    """Vista para la página de Contacto"""
    return render(request, 'contact.html')


def register(request):
    """Vista para la página de Registro"""
    return render(request, 'register.html')


def login(request):
    """Vista para la página de Inicio de Sesión"""
    return render(request, 'login.html')


def terms(request):
    """Vista para la página de Términos y Condiciones"""
    return render(request, 'terms.html')
