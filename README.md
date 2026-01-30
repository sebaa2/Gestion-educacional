# Portal Académico - Sistema de Gestión Educativa
Un sistema de gestión académica completo desarrollado con Django que facilita la administración escolar y conecta a estudiantes, profesores y administradores.
## 📋 Descripción
Portal Académico es una plataforma web diseñada para modernizar la gestión educativa, permitiendo:

## Gestión de estudiantes, profesores y cursos
- Administración de calificaciones y asistencia
- Distribución de materiales de estudio
- Asignación y seguimiento de tareas y pruebas
- Creación y visualización de horarios

#  ✨ Características Principales
Para Administradores

- ✅ Gestión completa de estudiantes y profesores
- 📚 Administración de cursos y asignaturas
- 📅 Creación de horarios personalizados por curso
- 📊 Dashboard con estadísticas del sistema
- 🔧 Control total sobre la estructura académica

## Para Profesores

- 📝 Subir material de estudio y recursos
- 📋 Crear y asignar tareas
- 📄 Crear y gestionar pruebas
- 💯 Asignar calificaciones a estudiantes
- 👀 Ver pruebas realizadas por estudiantes

## Para Estudiantes

- 📖 Acceso a materiales de estudio
- ✍️ Ver tareas asignadas
- 📝 Subir pruebas completadas
- 📊 Consultar calificaciones
- 🕐 Visualizar horarios de clase

# 🛠️ Tecnologías Utilizadas

- Backend: Django 5.1
- Base de Datos: SQLite (desarrollo) / PostgreSQL (producción recomendada)

- Frontend:
- Bootstrap 5.3.3
- Tailwind CSS
- HTML5, CSS3

- JavaScript: jQuery, DataTables, Chart.js

## 📦 Instalación
- Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- virtualenv (recomendado)

## Pasos de Instalación
```
Clonar el repositorio

bashgit clone <url-del-repositorio>
cd proyectodb

Crear y activar entorno virtual

bash# En Windows
python -m venv venv
venv\Scripts\activate

# En Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

## Instalar dependencias
```
bashpip install django
pip install --break-system-packages pillow  # Para manejo de imágenes

Aplicar migraciones

bashpython manage.py migrate

Crear superusuario (opcional)

bashpython manage.py createsuperuser

Ejecutar el servidor de desarrollo

bashpython manage.py runserver
```
## Acceder a la aplicación
```
http://localhost:8000
📁 Estructura del Proyecto
proyectodb/
├── adminapp/              # Aplicación de administración
│   ├── views.py          # Vistas del administrador
│   └── ...
├── appproject/           # Aplicación principal
│   ├── models.py         # Modelos de datos
│   ├── forms.py          # Formularios
│   ├── views.py          # Vistas de estudiantes
│   └── ...
├── profesorapp/          # Aplicación de profesores
│   ├── views.py          # Vistas del profesor
│   └── ...
├── templates/            # Plantillas HTML
│   ├── Base.html
│   ├── Panel_admin.html
│   ├── Panel_profesor.html
│   ├── Panel_estudiantes.html
│   └── ...
├── static/              # Archivos estáticos
│   ├── css/
│   ├── js/
│   └── images/
└── manage.py
💾 Modelos de Datos
```
## Principales Modelos
```
Estudiante: Información personal, curso asignado, credenciales
Profesor: Datos del docente, materias asignadas
Administrador: Usuarios con permisos administrativos
Curso: Estructura de cursos con asignaturas
Clases: Asignaturas individuales
Calificación: Notas de estudiantes
Tarea: Asignaciones para estudiantes
Prueba: Exámenes y evaluaciones
Documento: Material de estudio
Horario: Programación de clases
Asistencia: Registro de asistencia
```
## 🚀 Uso del Sistema
```
Acceso Inicial

Página Principal: http://localhost:8000/
Tres tipos de usuarios:

Estudiante: /Login_estudiante/
Profesor: /Login_profesor/
Administrador: /Login_admin/
```
