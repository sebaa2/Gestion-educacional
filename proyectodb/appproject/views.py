from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404, render, redirect
from .models import Estudiante, Calificacion
from datetime import datetime, timezone
from .forms import LoginForm 
    
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
            #En caso de que la contraseña ingresada sea igual a la contraseña almacenada
            if user.contraseña == password:
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
    return render(request, 'login_estudiantes.html', {'form': form})


def logout(request):
    request.session.pop('autenticado',None)
    return redirect('login_estudiantes')

#parte de estudiantes
def panel_estudiantes(request):
    if not request.session.get('autenticado'):
        return redirect('login_estudiantes')
    return render(request, 'Panel_estudiantes.html')


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

