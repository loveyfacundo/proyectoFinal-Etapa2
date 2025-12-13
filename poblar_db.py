"""
Script para poblar la base de datos de TodoDeporte con datos de ejemplo.

🎓 USO:
1. Coloca este archivo en la raíz del proyecto (junto a manage.py)
2. Tenes activo el entorno virtual
3. Ejecuta: python populate_db.py

IMPORTANTE: Este script borrará todos los datos existentes y creará datos nuevos.
"""

import os
import django
import sys

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todoDeporte.settings')
django.setup()

from django.contrib.auth.models import User
from apps.blog.models import Categoria, Perfil, Articulo, AcercaDe
from datetime import datetime, timedelta
import random


def limpiar_base_datos():
    """Elimina todos los datos existentes (excepto superusuarios)"""
    print("🗑️  Limpiando base de datos...")
    
    # Borrar artículos y comentarios
    Articulo.objects.all().delete()
    
    # Borrar usuarios que no sean superusuarios
    User.objects.filter(is_superuser=False).delete()
    
    # Borrar categorías
    Categoria.objects.all().delete()
    
    print("✓ Base de datos limpiada\n")


def crear_categorias():
    """Crea las categorías deportivas"""
    print("📂 Creando categorías...")
    
    categorias_data = [
        {
            'nombre': 'Fútbol',
            'descripcion': 'Noticias sobre fútbol nacional e internacional'
        },
        {
            'nombre': 'Básquet',
            'descripcion': 'Todo sobre básquetbol profesional y amateur'
        },
        {
            'nombre': 'Tenis',
            'descripcion': 'Grand Slams, ATP, WTA y más'
        },
        {
            'nombre': 'Fórmula 1',
            'descripcion': 'El mundo del automovilismo de alta velocidad'
        },
        {
            'nombre': 'Vóley',
            'descripcion': 'Voleibol nacional e internacional'
        },
        {
            'nombre': 'Rugby',
            'descripcion': 'Los Pumas y el rugby mundial'
        }
    ]
    
    categorias = []
    for cat_data in categorias_data:
        cat, created = Categoria.objects.get_or_create(
            nombre=cat_data['nombre'],
            defaults={'descripcion': cat_data['descripcion']}
        )
        categorias.append(cat)
        print(f"  ✓ {cat.nombre}")
    
    print(f"✓ {len(categorias)} categorías creadas\n")
    return categorias


def crear_usuarios():
    """Crea usuarios de ejemplo con diferentes roles"""
    print("👥 Creando usuarios...")
    
    usuarios_data = [
        {
            'username': 'colaborador1',
            'email': 'colaborador1@tododeporte.com',
            'first_name': 'María',
            'last_name': 'González',
            'password': 'asd123456',
            'rol': 'colaborador'
        },
        {
            'username': 'colaborador2',
            'email': 'colaborador2@tododeporte.com',
            'first_name': 'Juan',
            'last_name': 'Pérez',
            'password': 'asd123456',
            'rol': 'colaborador'
        },
        {
            'username': 'miembro1',
            'email': 'miembro1@tododeporte.com',
            'first_name': 'Ana',
            'last_name': 'Martínez',
            'password': 'asd123456',
            'rol': 'miembro'
        },
        {
            'username': 'miembro2',
            'email': 'miembro2@tododeporte.com',
            'first_name': 'Carlos',
            'last_name': 'López',
            'password': 'asd123456',
            'rol': 'miembro'
        },
        {
            'username': 'administrador1',
            'email': 'administrador1@tododeporte.com',
            'first_name': 'Pedro',
            'last_name': 'Hernandez',
            'password': 'asd123456',
            'rol': 'administrador'
        }
    ]
    
    usuarios = []
    for user_data in usuarios_data:
        # Crear usuario
        user, created = User.objects.get_or_create(
            username=user_data['username'],
            defaults={
                'email': user_data['email'],
                'first_name': user_data['first_name'],
                'last_name': user_data['last_name']
            }
        )
        
        if created:
            user.set_password(user_data['password'])
            user.save()
            
            # El perfil se crea automáticamente por las señales
            # Solo necesitamos actualizar el rol si es colaborador
            if user_data['rol'] == 'colaborador':
                perfil = user.perfil
                perfil.rol = 'colaborador'
                perfil.save()
        
        usuarios.append(user)
        rol_emoji = "✏️" if user_data['rol'] == 'colaborador' else "👤"
        print(f"  {rol_emoji} {user.get_full_name()} (@{user.username}) - {user_data['rol']}")
    
    print(f"✓ {len(usuarios)} usuarios creados")
    print("  📌 Contraseña para todos: asd123456\n")
    return usuarios


def crear_articulos(categorias, usuarios):
    """Crea artículos de ejemplo"""
    print("📰 Creando artículos...")
    
    # Filtrar solo colaboradores
    colaboradores = [u for u in usuarios if hasattr(u, 'perfil') and u.perfil.rol == 'colaborador']
    
    articulos_data = [
        # FÚTBOL
        {
            'titulo': 'Messi rompe otro récord en el Inter Miami',
            'contenido': '''Lionel Messi continúa escribiendo historia en la MLS. El astro argentino alcanzó su gol número 850 en su carrera profesional tras marcar un doblete en la victoria del Inter Miami por 3-1 ante Orlando City.

El primer gol llegó a los 23 minutos tras una asistencia de Jordi Alba, mientras que el segundo fue un tiro libre magistral a los 67 minutos que dejó sin opciones al arquero rival.

Con esta actuación, Messi se consolida como el máximo goleador extranjero en la historia de la MLS en una sola temporada, superando las expectativas desde su llegada al fútbol estadounidense.

El técnico Gerardo Martino destacó: "Leo sigue demostrando por qué es el mejor. Su influencia va más allá de los números, eleva el nivel de todo el equipo."

El Inter Miami se mantiene en la cima de la Conferencia Este con 67 puntos, a falta de cuatro jornadas para el final de la temporada regular.''',
            'categoria': 'Fútbol',
            'destacado': True
        },
        {
            'titulo': 'Ubeda, el apuntado por La Bombonera tras la eliminación de Boca ante Racing',
            'contenido': '''Boca perdió 1-0 con Racing en las semifinales del Torneo Clausura 2025 y Claudio Ubeda fue el gran apuntado por La Bombonera tras la eliminación.

El Xeneize jugó un primer tiempo aceptable ante La Academia, aunque prácticamente no pateó al arco. En la segunda etapa, el conjunto local se apagó, dejó crecer a Racing y fue víctima del regreso al gol de Adrián Maravilla Martínez.''',
            'categoria': 'Fútbol',
            'destacado': True
        },
        {
            'titulo': 'Argentina convoca a juveniles para el Sudamericano Sub-20',
            'contenido': '''La Selección Argentina Sub-20 dio a conocer la lista de convocados para el Campeonato Sudamericano que se disputará en Venezuela el próximo mes.
Javier Mascherano, técnico del combinado albiceleste, incluyó en la nómina a varias promesas que vienen destacándose en el fútbol local y europeo.
Entre los nombres más resonantes figuran Claudio Echeverri (River Plate), Franco Mastantuono (River Plate) y Agustín Ruberto (River Plate), considerados las joyas del fútbol argentino juvenil.
"Es un grupo con mucho talento y hambre de triunfo", expresó Mascherano en conferencia de prensa. "El objetivo es claro: clasificar al Mundial Sub-20 y hacerlo de la mejor manera posible."
El Sudamericano arranca el 23 de enero y Argentina integra el Grupo B junto a Brasil, Colombia, Ecuador y Paraguay.''',
            'categoria': 'Fútbol',
            'destacado': False
        },
        {
            'titulo': 'Eduardo Domínguez: Llegaron a la final dos de los mejores equipos del país',
            'contenido': '''Estudiantes eliminó a Gimnasia en las semifinales del Torneo Clausura 2025 por el triunfo por 1-0 y ahora jugará la final, en la que espera Racing. Eduardo Domínguez, DT del Pincha, analizó y celebró la clasificación al duelo decisivo.''',
            'categoria': 'Fútbol',
            'destacado': False
        },
        
        # BÁSQUET
        {
            'titulo': 'Campazzo brilla en su regreso a la NBA',
            'contenido': '''Facundo Campazzo tuvo una destacada actuación en su primer partido tras regresar a la NBA. El base cordobés aportó 14 puntos, 8 asistencias y 4 rebotes en los 28 minutos que estuvo en cancha.

El equipo de Campazzo se impuso por 112-98 ante los Milwaukee Bucks, en un partido donde el argentino demostró por qué es considerado uno de los mejores armadores sudamericanos de la historia.

"Estoy muy feliz de estar de vuelta", declaró Facu al término del encuentro. "Extrañaba mucho competir al máximo nivel y mi familia está feliz también."

El entrenador Steve Kerr elogió el desempeño del argentino: "Facundo nos dio exactamente lo que necesitábamos: ritmo, defensa y liderazgo en momentos clave."

Los números de Campazzo en el Real Madrid la temporada pasada (16.4 puntos y 7.1 asistencias promedio) convencieron a la franquicia para darle una nueva oportunidad en la mejor liga del mundo.''',
            'categoria': 'Básquet',
            'destacado': True
        },
        {
            'titulo': 'Liga Nacional: Obras Basket se consagra campeón',
            'contenido': '''Obras Basket se proclamó campeón de la Liga Nacional de Básquet tras vencer a Quimsa por 4-2 en la serie final.

El equipo dirigido por Gonzalo García selló el título con una victoria contundente por 91-75 en el Estadio Obras Sanitarias, ante una multitud que colmó las instalaciones.

Leandro Bolmaro fue la gran figura de la final con 27 puntos, 6 rebotes y 5 asistencias, siendo elegido como el MVP de las finales.

"Es un sueño hecho realidad para todos nosotros", expresó Bolmaro emocionado. "Este título es para toda la gente de Obras que nos apoyó incondicionalmente."

Con este campeonato, Obras Basket suma su tercer título en la Liga Nacional y se clasifica automáticamente a la próxima edición de la Basketball Champions League Americas.''',
            'categoria': 'Básquet',
            'destacado': False
        },
        
        # TENIS
        {
            'titulo': 'Sebastián Báez avanza a cuartos de final en Roland Garros',
            'contenido': '''El tenista argentino Sebastián Báez dio el golpe en París al vencer al número 5 del mundo en cuatro sets (6-4, 3-6, 7-6, 6-2) y clasificarse a los cuartos de final de Roland Garros.

Báez, de 23 años, mostró un tenis sólido y contundente ante uno de los mejores jugadores del circuito, aprovechando sus mejores armas: la devolución y el físico privilegiado en la arcilla.

"Es el triunfo más importante de mi carrera", afirmó Báez tras el partido. "Jugué con mucha confianza y pude sostener el nivel en los momentos clave."

En cuartos de final enfrentará al ganador del duelo entre Novak Djokovic y Lorenzo Musetti. De superar esa instancia, Báez se convertiría en el primer argentino en semifinales de Roland Garros desde Juan Martín del Potro en 2018.

La actuación de Báez genera gran expectativa en Argentina, donde el tenis vuelve a tener un representante de jerarquía mundial.''',
            'categoria': 'Tenis',
            'destacado': True
        },
        
        # FÓRMULA 1
        {
            'titulo': 'Colapinto cerca de conseguir un asiento para la próxima temporada',
            'contenido': '''Franco Colapinto estaría muy cerca de asegurar un lugar como piloto titular en la próxima temporada de Fórmula 1. Según fuentes cercanas al paddock, dos equipos habrían presentado ofertas formales al piloto argentino.

El joven de 21 años viene realizando una temporada destacada como piloto de reserva y desarrollo, completando miles de kilómetros en los test de mitad de semana y demostrando un ritmo competitivo.

"Franco ha impresionado a todos con su velocidad y madurez", comentó un representante de uno de los equipos interesados. "Definitivamente está listo para el desafío de la F1."

De concretarse, Colapinto se convertiría en el primer piloto argentino titular en Fórmula 1 desde Gastón Mazzacane en 2001, un hito histórico para el automovilismo nacional.

Las negociaciones están en etapa avanzada y se espera que haya novedades en las próximas semanas, antes del cierre de la temporada actual.''',
            'categoria': 'Fórmula 1',
            'destacado': False
        },
        {
            'titulo': 'Lando Norris es el campeón de F1, pero: ¿es un gran campeón?',
            'contenido': '''El inglés terminó con el reinado de Max Verstappen al consagrarse con su McLaren, pero es un piloto que por ahora no emociona ni genera fanatismo.
            “Todos los años hay un campeón, pero no siempre hay un gran campeón”. La frase la inmortalizó Ayrton Senna. La temporada 2025 de Fórmula 1 tuvo, como debía ser, un campeón: Lando Norris. La gran pregunta, parafraseando al enorme piloto brasileño es: ¿hubo un gran campeón?''',
            'categoria': 'Fórmula 1',
            'destacado': False
        },
        
        # VÓLEY
        {
            'titulo': 'La selección argentina de vóley masculino se clasifica al Mundial',
            'contenido': '''Argentina logró su clasificación al Mundial de Voleibol tras vencer a Chile por 3-0 (25-19, 25-22, 25-17) en el partido decisivo del Sudamericano disputado en Santiago.

El equipo dirigido por Marcelo Méndez mostró un nivel superlativo durante todo el torneo, finalizando invicto con 6 victorias en igual cantidad de presentaciones.

Luciano De Cecco, capitán del seleccionado, fue la figura del partido con 12 puntos y una dirección impecable del juego. "Estamos muy contentos por lograr el objetivo", declaró el experimentado armador.

Bruno Lima aportó 18 puntos en la victoria, consolidándose como el máximo anotador argentino del torneo con 96 puntos en total.

El Mundial se disputará en Polonia entre agosto y septiembre del próximo año, y Argentina buscará superar su mejor participación histórica (5° puesto en 1982).''',
            'categoria': 'Vóley',
            'destacado': False
        },
        
        # RUGBY
        {
            'titulo': 'Los Pumas derrotan a los All Blacks en histórico partido',
            'contenido': '''Argentina escribió una página dorada en su historia al vencer a Nueva Zelanda por 38-30 en un épico encuentro disputado en el Estadio Único de La Plata ante 53.000 espectadores.

Los Pumas dominaron desde el inicio con un juego inteligente y agresivo, aprovechando cada oportunidad para vulnerar la defensa neozelandesa. Tries de Santiago Carreras, Mateo Carreras y Pablo Matera encaminaron el triunfo argentino.

"Es una victoria histórica para el rugby argentino", expresó emocionado el capitán Julián Montoya. "El equipo jugó de manera perfecta y demostró que podemos competir de igual a igual con las mejores selecciones del mundo."

La bota de Emiliano Boffelli fue fundamental con 18 puntos producto de conversiones y penales en momentos clave del partido.

Con este resultado, Argentina se consolida en el segundo lugar del Rugby Championship y genera gran ilusión de cara al Mundial de Francia 2027.''',
            'categoria': 'Rugby',
            'destacado': False
        }
    ]
    
    articulos = []
    fecha_base = datetime.now()
    
    for i, art_data in enumerate(articulos_data):
        # Fecha progresivamente más antigua
        dias_atras = i * 2
        fecha = fecha_base - timedelta(days=dias_atras)
        
        # Asignar autor (alterna entre colaboradores)
        autor = colaboradores[i % len(colaboradores)]
        
        # Buscar la categoría
        categoria = Categoria.objects.get(nombre=art_data['categoria'])
        
        articulo = Articulo.objects.create(
            titulo=art_data['titulo'],
            contenido=art_data['contenido'],
            categoria=categoria,
            autor=autor,
            destacado=art_data['destacado'],
            fecha_creacion=fecha
        )
        articulos.append(articulo)
        
        emoji = "⭐" if articulo.destacado else "📄"
        print(f"  {emoji} {articulo.titulo[:50]}...")
    
    print(f"✓ {len(articulos)} artículos creados\n")
    return articulos


def crear_acerca_de():
    """Crea el contenido de la página Acerca de"""
    print("ℹ️  Creando página 'Acerca de'...")
    
    contenido = """TodoDeporte nació en 2025 como un proyecto del Informatorio Chaco, con la misión de acercar las mejores noticias deportivas a todos los argentinos.

Somos un equipo apasionado por el deporte en todas sus formas, comprometidos con ofrecer información precisa, análisis profundos y cobertura en tiempo real de los eventos más importantes.

Nuestra plataforma cubre fútbol, básquet, tenis, automovilismo, vóley, rugby y mucho más, siempre con la perspectiva argentina pero sin perder de vista el panorama internacional."""

    integrantes = """• Facundo Lovey - Programador
• Alejandro Martinez - Programador
• Dihué De Cuadra - Programador
• José Centurión - Programador"""

    acerca_de, created = AcercaDe.objects.get_or_create(
        id=1,
        defaults={
            'contenido': contenido,
            'integrantes': integrantes
        }
    )
    
    if not created:
        acerca_de.contenido = contenido
        acerca_de.integrantes = integrantes
        acerca_de.save()
    
    print("✓ Página 'Acerca de' creada\n")


def main():
    """Función principal que ejecuta todo"""
    print("\n" + "="*60)
    print("🚀 SCRIPT DE POBLACIÓN DE BASE DE DATOS - TODODEPORTE")
    print("="*60 + "\n")
    
    # Confirmar antes de proceder
    respuesta = input("⚠️  Este script borrará todos los datos existentes. ¿Continuar? (s/n): ")
    if respuesta.lower() != 's':
        print("Operación cancelada.")
        sys.exit(0)
    
    print("\n")
    
    try:
        # Ejecutar funciones en orden
        limpiar_base_datos()
        categorias = crear_categorias()
        usuarios = crear_usuarios()
        articulos = crear_articulos(categorias, usuarios)
        crear_acerca_de()
        
        print("="*60)
        print("✅ BASE DE DATOS POBLADA EXITOSAMENTE")
        print("="*60)
        print("\n📊 RESUMEN:")
        print(f"  • {len(categorias)} categorías")
        print(f"  • {len(usuarios)} usuarios (colaboradores y miembros)")
        print(f"  • {len(articulos)} artículos")
        print(f"  • {sum(1 for a in articulos if a.destacado)} artículos destacados")
        
        print("\n🔐 CREDENCIALES DE ACCESO:")
        print("  Username: colaborador1")
        print("  Password: password123")
        print("\n  Username: miembro1")
        print("  Password: password123")
        
        print("\n💡 PRÓXIMOS PASOS:")
        print("  1. Ejecuta: python manage.py runserver")
        print("  2. Visita: http://localhost:8000")
        print("  3. Inicia sesión con las credenciales anteriores")
        print("  4. ¡Explora tu blog TodoDeporte!\n")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("\nAsegúrate de que:")
        print("  • El servidor NO esté corriendo (python manage.py runserver)")
        print("  • Las migraciones estén aplicadas (python manage.py migrate)")
        sys.exit(1)


if __name__ == '__main__':
    main()