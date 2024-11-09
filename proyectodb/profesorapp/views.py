from django.shortcuts import get_object_or_404, render, redirect
from appproject.models import Profesor, Estudiante, Calificacion, Clases, Curso
from appproject.forms import LoginForm, CalificacionForm
from django.urls import reverse

def Principal(request):
    return render(request, 'Principal.html')

def login_profesor(request):
    form = LoginForm(request.POST)
    if request.method =="POST" and form.is_valid(): 
        #Asociamos las variables del formulario a variables de la función
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        try:
            user = Profesor.objects.get(rut = username)
            #En caso de que la contraseña ingresada sea igual a la contraseña almacenada
            if user.contraseña == password:
                request.session['autenticado'] = True 
                request.session['usuario'] = user.rut 
                request.session['usuario_id'] = user.idProfesor
                request.session['nombre_completo'] = user.nombre +" "+ user.apellido
                #Redireccionamos a lista de gestiones
                return redirect("/Panel_profesor")
            else:
                form.add_error(None, 'Contraseña incorrecta')
        except Profesor.DoesNotExist:
            form.add_error(None, 'Usuario no existe')
    return render(request, "Login_profesor.html", {"form": form, 'title': 'login_profesor', 'home_url': '/'})

def panel_profesor(request):
    #Verificamos si la variable de autenticacion existe
    if not request.session.get('autenticado'):
        return redirect('Login_profesor')
    return render(request, 'Panel_profesor.html')

def logout_profesor(request):
    request.session.pop('autenticado',None)
    return redirect('login_profesor')

#cambios en este metodo enfocado en las notas, falta testeo 
def agregar_calificacion(request, clase_id):
    # Verificar si el profesor está autenticado
    if not request.session.get('autenticado'):
        return redirect('login_profesor')

    # Obtener el profesor y la clase seleccionada
    profesor_id = request.session.get('usuario_id')
    profesor = get_object_or_404(Profesor, idProfesor=profesor_id)
    clase = get_object_or_404(Clases, idClases=clase_id, profesor=profesor)

    if request.method == 'POST':
        form = CalificacionForm(request.POST)
        if form.is_valid():
            calificacion = form.save(commit=False)
            calificacion.profesor = profesor
            calificacion.clase = clase  # Asignar la clase automáticamente
            calificacion.save()
            return redirect('listar_calificaciones')  # Redirigir al listado de clases

    else:
        form = CalificacionForm()

    return render(request, 'Agregar_calificacion.html', {
        'form': form,
        'clase': clase,
        'nombre_completo': request.session.get('nombre_completo'),'title':'panel_profesor',
        'home_url':reverse('panel_profesor')
    })

def clases_del_profesor(request):
    # Verifica si el profesor está autenticado
    if not request.session.get('autenticado'):
        return redirect('ruta_de_login')  # Redirige al login si no está autenticado

    profesor_id = request.session.get('usuario_id')
    
    # Obtén las clases asociadas al profesor logueado
    clases = Clases.objects.filter(profesor_id=profesor_id)

    return render(request, 'Plantillas_asignaturas.html', {'clases': clases, 'title':'panel_profesor',
        'home_url':reverse('panel_profesor')})

def cursos_del_profesor(request):
    if not request.session.get('autenticado'):
        return redirect('ruta_de_login')  # Redirige al login si no está autenticado
    
    profesor_id = request.session.get('usuario_id')
    
    # Filtrar los cursos que tienen clases asignadas a este profesor
    cursos = Curso.objects.filter(clases__profesor_id=profesor_id).distinct()
    
    # Imprimir los cursos para verificar
    print(cursos)  # Verifica que la lista no esté vacía
    
    return render(request, 'Plantillas_curso.html', {'cursos': cursos ,'title':'panel_profesor',
        'home_url':reverse('panel_profesor')})

def listar_calificaciones(request):
    # Verifica si el profesor está autenticado
    if not request.session.get('autenticado'):
        return redirect('ruta_de_login')

    # Obtener el ID del profesor desde la sesión
    profesor_id = request.session.get('usuario_id')

    # Filtrar las calificaciones ingresadas por el profesor
    calificaciones = Calificacion.objects.filter(profesor_id=profesor_id).select_related('estudiante', 'clase', 'curso')

    return render(request, 'Listar_calificaciones.html', {
        'calificaciones': calificaciones,
        'nombre_completo': request.session.get('nombre_completo'),'title':'panel_profesor',
        'home_url':reverse('panel_profesor')
    })


