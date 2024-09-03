from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from .models import Estudiante, Asistencia
from datetime import datetime
from .forms import LoginForm

#panel de estudiantes

def Asistencias_estudiantes(request):
    idEstudiante = request.session.get('usuario')
    if not idEstudiante:
        return redirect('login_estudiantes')  # Redirige al login si no está autenticado

    asistencia = Asistencia.objects.filter(estudiante_id=idEstudiante)
    return render(request, 'Asistencia_estudiantes.html', {'asistencia': asistencia})


def lista_estudiantes(request):
    estudiantes = Estudiante.objects.all()
    return render(request,'Lista_estudiantes.html', {'estudiantes': estudiantes})

def Agregar_estudiantes(request):
    return render(request, 'Agregar_estudiantes.html')

def Registrar_estudiantes(request):
    if request.method == 'POST':
        nombres = request.POST.get('txtestudiante', '')
        apellidos = request.POST.get('txtapellidos', '')
        fecha_nacimiento = request.POST.get('txtfechan', '')
        direccion = request.POST.get('txtdireccion', '')
        telefono = request.POST.get('txtfono', '')
        matricula = request.POST.get('txtfechai', '')
        rut = request.POST.get('txtrut', '')
        contraseña = request.POST.get('txtpassword', '')

        # Validar y convertir las fechas
        if fecha_nacimiento:
            try:
                fecha_nacimiento = datetime.strptime(fecha_nacimiento, '%Y-%m-%d').date()
            except ValueError:
                return HttpResponse("Error en la fecha de nacimiento")

        if matricula:
            try:
                matricula = datetime.strptime(matricula, '%Y-%m-%d').date()
            except ValueError:
                return HttpResponse("Error en la fecha de inscripción")

        # Crear y guardar el objeto Estudiante
        registro = Estudiante.objects.create(
            nombre=nombres,
            apellido=apellidos,
            fecha_nacimiento=fecha_nacimiento,
            direccion=direccion,
            telefono=telefono,
            matricula=matricula,
            rut=rut,
            contraseña=contraseña
        )
        registro.save()
    return redirect('Lista_estudiantes/')

def Eliminar_estudiantes(request, idEstudiante):
    estudiante = Estudiante.objects.get(idEstudiante=idEstudiante)
    estudiante.delete()
    return redirect('/')

def Actualizar_estudiantes(request, idEstudiante):
    estudiante = get_object_or_404(Estudiante, id=idEstudiante)
    return render(request, "Actualizar_estudiantes.html", {'estudiante': estudiante})

def Editar_estudiante(request, idEstudiante):
    if request.method == 'POST':
        nombres = request.POST.get('txtestudiante', '')
        apellidos = request.POST.get('txtapellidos', '')
        fecha_nacimiento = request.POST.get('txtfechan', '')
        direccion = request.POST.get('txtdireccion', '')
        telefono = request.POST.get('txtfono', '')
        fecha_inscripcion = request.POST.get('txtfechai', '')

        estudiante = get_object_or_404(Estudiante, idEstudiante=idEstudiante)
        estudiante.nombre = nombres
        estudiante.apellido = apellidos
        estudiante.fecha_nacimiento = fecha_nacimiento
        estudiante.direccion = direccion
        estudiante.telefono = telefono
        estudiante.fecha_inscripcion = fecha_inscripcion
        estudiante.save()
        return redirect('/')
    else:
        estudiante = get_object_or_404(Estudiante, idEstudiante=idEstudiante)
        return render(request, 'Actualizar_estudiantes.html', {'estudiante': estudiante})
    
def Principal(request):
    return render(request, 'Principal.html')

def login_view(request):
    form = LoginForm(request.POST)
    if request.method =="POST" and form.is_valid(): 
        #Asociamos las variables del formulario a variables de la función
        txt_usuario = form.cleaned_data.get("txt_username")
        txt_password = form.cleaned_data.get("txt_password")
        try:
            user = Estudiante.objects.get(rut = txt_usuario)
            #En caso de que la contraseña ingresada sea igual a la contraseña almacenada
            if user.contraseña == txt_password:
                request.session['autenticado'] = True 
                request.session['usuario'] = user.rut 
                request.session['nombre_completo'] = user.nombre +" "+ user.apellido
                #Redireccionamos a lista de gestiones
                return redirect("/Panel_estudiantes")
            else:
                form.add_error(None, 'Contraseña incorrecta')
        except Estudiante.DoesNotExist:
            form.add_error(None, 'Usuario no existe')
    return render(request, "Login_estudiantes.html", {"form": form})

def logout(request):
    request.session.pop('autenticado',None)
    return redirect('/login')

def panel_estudiantes(request,):
    return render(request, 'Panel_estudiantes.html')