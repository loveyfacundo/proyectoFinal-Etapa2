# 📝 Proyecto Blog en Django

Este proyecto es una aplicación web tipo **blog**, desarrollada con el framework **Django**, como entrega final de la **Etapa 2 del Informatorio 2025**.  
La aplicación cuenta con un sistema de usuarios con distintos perfiles y permite gestionar artículos y comentarios, además de ofrecer navegación y filtrado de contenidos.

---

## 🚀 Objetivo del Proyecto

Desarrollar una aplicación web completa utilizando **Django**, cumpliendo con los requisitos funcionales y de diseño establecidos, y publicarla de manera online en el hosting gratuito:

➡️ https://www.pythonanywhere.com/

---

## 👥 Perfiles de Usuario

Además del **superusuario** propio de Django, la aplicación incluye tres perfiles adicionales:

### 🔹 Visitante
- Navega libremente por la web.
- Filtra publicaciones.
- Lee artículos.
- Puede registrarse y loguearse.

### 🔹 Miembro / Usuario Registrado
Incluye todas las capacidades del Visitante, y además:
- Comenta artículos.
- Edita o elimina sus propios comentarios.
- Puede desloguearse.

### 🔹 Colaborador
Dispone de permisos avanzados para gestionar contenido:
- Crear, editar y eliminar artículos.
- Subir, editar y eliminar fotos asociadas.
- Categorizar artículos.
- Editar y eliminar comentarios de otros usuarios.

---

## 🧩 Funcionalidades Principales

### ✏️ Gestión de Artículos
- Crear, leer, editar y eliminar publicaciones.
- Subir imágenes asociadas a los artículos.
- Asignar categorías.

### 💬 Gestión de Comentarios
- Crear, leer, editar y eliminar comentarios.
- Los miembros solo pueden editar/eliminar los suyos.
- Los colaboradores pueden editar/eliminar comentarios ajenos.

### 🔍 Filtros Disponibles
Las publicaciones se pueden filtrar por:
- Categoría
- Antigüedad (asc / desc)
- Orden alfabético (asc / desc)

### 🔐 Autenticación
- Registro de usuarios
- Login
- Logout

---

## 📂 Secciones del Sitio

### 🏠 Inicio / Portada
Muestra una selección de artículos recientes o destacados para ofrecer una visión general del contenido disponible.

### 🗂️ Categorías
Organiza los artículos en distintas temáticas para facilitar la navegación.

### ℹ️ Acerca de
Incluye información sobre el proyecto, su propósito y los autores.

### ✉️ Contacto
Proporciona medios para comunicarse con el equipo del blog.

---

## 🛠️ Tecnologías Utilizadas

- Python 3.13  
- Django 5.2  
- HTML5 / CSS3  
- SQLite  

---

## 🌐 Despliegue en PythonAnywhere

El proyecto estará publicado en el hosting gratuito:

➡️ https://www.pythonanywhere.com/

---

## 📦 Instalación y Uso en Local

### 1️⃣ Clonar el repositorio
```bash
git clone https://github.com/loveyfacundo/proyectoFinale-Etapa2.git
```
```bash
cd proyectoFinale-Etapa2
```

### 2️⃣ Crear y activar el entorno virtual
```bash
python -m venv venv
```
```bash
source venv/bin/activate   # Linux / Mac
```
```bash
venv\Scripts\activate      # Windows
```

### 3️⃣ Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4️⃣ Ejecutar migraciones
```bash
python manage.py migrate
```

### 5️⃣ Crear superusuario
```bash
python manage.py createsuperuser
```

### 6️⃣ Ejecutar el servidor
```bash
python manage.py runserver
```

---

## 📄 Licencia

Este proyecto está licenciado bajo los términos de la licencia **MIT**.
Consultá el archivo **LICENSE** para más información.
