from datetime import timezone
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from appproject.models import Profesor, Estudiante, Calificacion, Clases, Curso, Prueba, PruebaSubida
from appproject.forms import LoginForm, DocumentoForm, TareaForm, PruebaForm, FiltroNotasForm
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

def Eliminar_calificacion(request, idCalificacion):
    calificacion = get_object_or_404(Calificacion, idCalificacion=idCalificacion)
    calificacion.delete()
    return redirect('listar_calificaciones')

def subir_documento(request):
    if not request.session.get('autenticado', False):
        return redirect('login_profesor')  # Redirigir si el profesor no está autenticado

    # Get the logged-in professor's ID
    profesor_id = request.session.get('usuario_id')

    if request.method == 'POST':
        # Create the form with filtered choices for the specific professor
        form = DocumentoForm(request.POST, request.FILES, profesor_id=profesor_id)
        if form.is_valid():
            # Asociar el profesor autenticado al documento
            documento = form.save(commit=False)
            # Obtener el profesor desde la sesión
            documento.profesor_id = profesor_id
            documento.save()
            return redirect('panel_profesor')  # Redirige a una página de éxito
    else:
        # Create the form with filtered choices for the specific professor
        form = DocumentoForm(profesor_id=profesor_id)

    return render(request, 'subir_documento.html', {'form': form})

def asignar_tarea(request):
    if request.method == 'POST':
        form = TareaForm(request.POST)
        if form.is_valid():
            tarea = form.save(commit=False)  # No guardar todavía
            profesor = Profesor.objects.get(rut=request.session['usuario'])  # Obtener el profesor según el rut guardado en la sesión
            tarea.profesor = profesor  # Asignar el profesor a la tarea
            tarea.save()  # Ahora sí guardar la tarea con el profesor asignado
            return redirect('panel_profesor')  # Redirigir al panel del profesor
        else:
            print(form.errors)  # Ver los errores del formulario
    else:
        form = TareaForm()
    return render(request, 'asignar_tarea.html', {'form': form})

def crear_prueba(request):
    if not request.session.get('autenticado'):  # Verificar si el profesor está autenticado
        return redirect('login_profesor')  # Redirigir al login si no está autenticado
    
    profesor_id = request.session.get('usuario_id')  # Obtener el ID del profesor desde la sesión

    if request.method == 'POST':
        form = PruebaForm(request.POST, request.FILES, profesor_id=profesor_id)
        if form.is_valid():
            prueba = form.save(commit=False)
            prueba.profesor_id = profesor_id  # Asignar el profesor autenticado
            prueba.save()
            return redirect('/Panel_profesor')  # Redirigir al panel del profesor después de crear la prueba
    else:
        form = PruebaForm(profesor_id=profesor_id)

    return render(request, 'crear_prueba.html', {'form': form, 'title': 'Crear Prueba'})

def filtrar_notas(request):
    if not request.session.get('autenticado'):  # Verificar autenticación
        return redirect('login_profesor')
    
    profesor_id = request.session.get('usuario_id')  # Obtener el ID del profesor
    form = FiltroNotasForm(request.GET or None, profesor_id=profesor_id)  # Pasar profesor_id

    estudiantes = []
    prueba = None

    if form.is_valid():
        curso = form.cleaned_data['curso']
        clase = form.cleaned_data['clase']
        prueba = form.cleaned_data['prueba']

        # Filtrar estudiantes asociados al curso
        estudiantes = Estudiante.objects.filter(curso=curso)

        # Crear calificaciones si no existen
        for estudiante in estudiantes:
            Calificacion.objects.get_or_create(
            estudiante=estudiante,
            prueba=prueba,
            curso=curso,
            clase=clase,
            profesor=prueba.profesor,
            defaults={'nota': 1},
            )
            return redirect(reverse('asignar_notas', args=[prueba.id]))

    return render(request, 'filtrar_notas.html', {
        'form': form,
        'estudiantes': estudiantes,
        'prueba': prueba,
    })

def asignar_notas(request, prueba_id):
    prueba = get_object_or_404(Prueba, id=prueba_id)
    estudiantes = Estudiante.objects.filter(curso=prueba.curso)

    if request.method == "POST":
        for estudiante in estudiantes:
            nota = request.POST.get(f'nota_{estudiante.idEstudiante}')
            if nota:
                calificacion, created = Calificacion.objects.get_or_create(
                    estudiante=estudiante,
                    prueba=prueba,
                    curso=prueba.curso,  
                    profesor=prueba.profesor,  
                    defaults={'nota': float(nota)}
                )
        if not created:
            calificacion.nota = float(nota)
            calificacion.save()
        return redirect('panel_profesor')

    return render(request, 'asignar_notas.html', {'prueba': prueba, 'estudiantes': estudiantes})

def ver_pruebas_realizadas(request):
    if not request.session.get('autenticado'):  # Verificar autenticación
        return redirect('login_profesor')

    pruebas_subidas = PruebaSubida.objects.all()  # Aquí puedes filtrar según el curso o materia del profesor

    return render(request, 'ver_pruebas_realizadas.html', {'pruebas_subidas': pruebas_subidas})