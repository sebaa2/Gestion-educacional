from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404, render, redirect
from .models import Estudiante, Calificacion, Clases, Documento, Tarea
from datetime import datetime, timezone
from .forms import LoginForm 
from django.urls import reverse
import os


def Principal(request):
    return render(request, 'Principal.html')

def login_view(request):
    form = LoginForm(request.POST)
    if request.method =="POST" and form.is_valid(): 
        #Asociamos las variables del formulario a variables de la función
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        try:
            user = Estudiante.objects.get( rut = username)
            #En caso de que la contrasena ingresada sea igual a la contrasena almacenada
            if user.contrasena == password:
                request.session['autenticado'] = True 
                request.session['usuario'] = user.rut
                request.session['usuario_id'] = user.idEstudiante 
                request.session['nombre_completo'] = user.nombre +" "+ user.apellido
                #Redireccionamos a lista de gestiones
                return redirect("panel_estudiantes")
            else:
                form.add_error(None, 'Contraseña incorrecta')
        except Estudiante.DoesNotExist:
            form.add_error(None, 'Usuario no existe')
    return render(request, 'login_estudiantes.html', {'form': form, 'title': 'login_estudiante', 'home_url': '/'})


def logout(request):
    request.session.pop('autenticado',None)
    return redirect('login_estudiantes')

#parte de estudiantes
def panel_estudiantes(request):
    if not request.session.get('autenticado'):
        return redirect('login_estudiantes')
    estudiante_id = request.session.get('usuario_id')
    if estudiante_id:
        # Obtener el estudiante usando el id de la sesión
        estudiante = Estudiante.objects.get(idEstudiante=estudiante_id)
        return render(request, 'Panel_estudiantes.html', {'estudiante': estudiante})
    else:
        # Si no se encuentra el id del estudiante, redirigir al login
        return redirect('login_estudiantes')


def panel_asignaturas_estudiante(request, idEstudiante):
    estudiante = get_object_or_404(Estudiante, idEstudiante=idEstudiante)

    # Obtener el curso del estudiante y sus asignaturas relacionadas
    curso = estudiante.curso
    clases = curso.clases.all() if curso else []  # Obtenemos las asignaturas del curso

    context = {
        'estudiante': estudiante,
        'clases': clases,
    }

    return render(request, 'panel_asignaturas_estudiante.html', context)

def calificaciones_estudiante(request):
    # Verificamos si el estudiante está autenticado
    if not request.session.get('autenticado'):
        return redirect('ruta_de_login')  # Redirigir al login si no está autenticado

    estudiante_id = request.session.get('usuario_id')  # Obtenemos el id del estudiante
    calificaciones = Calificacion.objects.filter(estudiante_id=estudiante_id)

    return render(request, 'Calificaciones_estudiante.html', {'calificaciones': calificaciones})

def horario_estudiante(request, estudiante_id):
    # Obtener al estudiante por ID
    estudiante = Estudiante.objects.get(idEstudiante=estudiante_id)
    
    # Obtener el curso al que pertenece
    curso = estudiante.curso
    
    # Obtener las clases asociadas a ese curso
    clases = curso.clases.all()
    
    # Crear una lista de horarios para cada clase
    horario = []
    for clase in clases:
        for fecha_horario in clase.fecha_horario.all():
            horario.append({
                'clase': clase.nombre,
                'hora_entrada': clase.hora_entrada,
                'hora_salida': clase.hora_salida,
                'dia': fecha_horario.nombre,
            })

    return render(request, 'horario_estudiante.html', {'horario': horario, 'estudiante': estudiante})

# views.py
def listar_documentos(request, curso_id=None, clase_id=None):
    if curso_id:
        documentos = Documento.objects.filter(curso_id=curso_id)
    elif clase_id:
        documentos = Documento.objects.filter(clase_id=clase_id)
    else:
        documentos = Documento.objects.all()
    
    return render(request, 'listar_documentos.html', {'documentos': documentos})

def descargar_documento(request, documento_id):
    documento = get_object_or_404(Documento, id=documento_id)
    archivo_path = documento.archivo.path  # Obtiene la ruta absoluta del archivo en el sistema de archivos
    
    with open(archivo_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(archivo_path)}"'
        return response

def ver_tareas(request):
    # Verificar si el usuario está autenticado
    if request.session.get('autenticado'):
        estudiante_id = request.session.get('usuario_id')
        estudiante = Estudiante.objects.get(idEstudiante=estudiante_id)
        tareas = Tarea.objects.filter(curso=estudiante.curso)  # Filtrar tareas según el curso del estudiante
        return render(request, 'ver_tareas.html', {'tareas': tareas})
    else:
        return redirect('login_estudiante')  # Redireccionar al login si no está autenticado
    
def plantilla_accionesprofe(request):
    documento = Documento.objects.first()  # Obtén un documento para el enlace de descarga
    return render(request, 'redirigir.html', {'documento': documento})
