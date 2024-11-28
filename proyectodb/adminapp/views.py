from django.shortcuts import render
from django.urls import reverse
from appproject.models import Administrador, Estudiante, Profesor, Curso, Clases
from appproject.forms import LoginForm, AgregarEstudiantes, AgregarProfesor, AgregarCursoForm, AgregarAsignaturas
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from datetime import datetime
from django.contrib.auth.decorators import login_required

def login_admin(request):
    form = LoginForm(request.POST)
    if request.method =="POST" and form.is_valid(): 
        #Asociamos las variables del formulario a variables de la función
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        try:
            user = Administrador.objects.get(rut = username)
            #En caso de que la contraseña ingresada sea igual a la contraseña almacenada
            if user.contraseña == password:
                request.session['autenticado'] = True 
                request.session['usuario'] = user.rut 
                request.session['nombre_completo'] = user.nombre +" "+ user.apellido
                #Redireccionamos a lista de gestiones
                return redirect("/Panel_admin")
            else:
                form.add_error(None, 'contraseña incorrecta')
        except Administrador.DoesNotExist:
            form.add_error(None, 'Usuario no existe')
    return render(request, "Login_admin.html", {"form": form,'title': 'login_admin', 'home_url': '/'})

#@login_required
def logout_admin(request):
    request.session.pop('autenticado',None)
    return redirect('Login_admin')

def panel_administrador(request,):
    if not request.session.get('autenticado'):
        return redirect('Login_admin')
    return render(request, 'Panel_admin.html')

def lista_asignaturas(request):
    asignaturas = Clases.objects.all()  # Obtiene todos los cursos de la base de datos
    return render(request, 'Lista_asignaturas.html', {'asignaturas': asignaturas, 'title': 'Panel_admin','home_url':reverse('Panel_admin')})

def agregar_asignatura(request):
    if request.method == 'POST':
        form = AgregarAsignaturas(request.POST)
        if form.is_valid():
            form.save()  # Guarda el nuevo curso en la base de datos
            return redirect('lista_asignaturas')  # Cambia a la URL correspondiente
    else:
        form = AgregarAsignaturas()  # Crea un formulario vacío
    return render(request, 'Agregar_asignatura.html', {'form': form, 'title': 'Panel_admin','home_url':reverse('Panel_admin')})

def lista_cursos(request):
    cursos = Curso.objects.all()  # Obtiene todos los cursos de la base de datos
    return render(request, 'Lista_cursos.html', {'cursos': cursos})

def agregar_curso(request):
    if request.method == 'POST':
        form = AgregarCursoForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda el nuevo curso en la base de datos
            return redirect('lista_cursos')  # Cambia a la URL correspondiente
    else:
        form = AgregarCursoForm()  # Crea un formulario vacío
    return render(request, 'Agregar_curso.html', {'form': form,'title': 'Panel_admin','home_url':reverse('Panel_admin')})

def lista_estudiantes(request):
    estudiantes = Estudiante.objects.all()
    return render(request,'Lista_estudiantes.html', {'estudiantes': estudiantes})

def Registrar_estudiantesForm(request):
    if request.method == 'POST':
        form = AgregarEstudiantes(request.POST)
        if form.is_valid():
            form.save()  # Guarda el nuevo estudiante en la base de datos
            return redirect('lista_estudiantes')  # Redirige a una página de éxito u otra vista
    else:
        form = AgregarEstudiantes()  # Instancia un formulario vacío
    return render(request, 'Agregar_estudiantes.html', {'form': form, 'title': 'Panel_admin','home_url':reverse('Panel_admin')})

def lista_profesores(request):
    profesores = Profesor.objects.all()  # Obtén todos los profesores
    return render(request, 'Lista_profesores.html', {'profesores': profesores, 'title': 'Panel_admin','home_url':reverse('Panel_admin')})

def Registrar_profesorForm(request):
    if request.method == 'POST':
        form = AgregarProfesor(request.POST)
        if form.is_valid():
            form.save()  # Guarda el nuevo profesor en la base de datos
            return redirect('Lista_profesores')  # Redirige a la lista de profesores o a otra vista
    else:
        form = AgregarProfesor()  # Instancia un formulario vacío
    return render(request, 'agregar_profesor.html', {'form': form, 'title': 'Panel_admin','home_url':reverse('Panel_admin')})

def Eliminar_estudiantes(request, idEstudiante):
    estudiante = get_object_or_404(Estudiante, idEstudiante=idEstudiante)
    estudiante.delete()
    return redirect('lista_estudiantes')

def Eliminar_profesor(request, idProfesor):
    profesor = get_object_or_404(Profesor, idProfesor=idProfesor)
    profesor.delete()
    return redirect('Lista_profesores')

def Eliminar_curso(request, idCurso): 
    curso = get_object_or_404(Curso, idCurso=idCurso) # con el id del podemos elimniar de la base de datos
    curso.delete()
    return redirect('lista_cursos')

def Eliminar_asignatura(request, idClases):
    clases = get_object_or_404(Clases, idClases=idClases)
    clases.delete()
    return redirect('lista_asignaturas')

def editar_estudiante(request, idEstudiante):
    # Obtener el estudiante por ID
    estudiante = get_object_or_404(Estudiante, idEstudiante=idEstudiante)

    if request.method == "POST":
        # Llenar el formulario con los datos enviados y el estudiante actual
        form = AgregarEstudiantes(request.POST, instance=estudiante)
        if form.is_valid():
            form.save()  # Guardar cambios
            return redirect('lista_estudiantes')  # Redirigir a la lista de estudiantes
    else:
        # Prellenar el formulario con los datos actuales del estudiante
        form = AgregarEstudiantes(instance=estudiante)

    # Renderizar el formulario en la plantilla
    return render(request, 'Actualizar_estudiantes.html', {
        'form': form,
        'title': 'Editar Estudiante',
        'home_url': reverse('Panel_admin'),
    })
