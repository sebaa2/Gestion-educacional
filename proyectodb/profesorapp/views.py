from django.shortcuts import get_object_or_404, render, redirect
from appproject.models import Profesor, Estudiante, Calificacion
from appproject.forms import LoginForm, CalificacionForm

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
                request.session['nombre_completo'] = user.nombre +" "+ user.apellido
                #Redireccionamos a lista de gestiones
                return redirect("/Panel_profesor")
            else:
                form.add_error(None, 'Contraseña incorrecta')
        except Profesor.DoesNotExist:
            form.add_error(None, 'Usuario no existe')
    return render(request, "Login_profesor.html", {"form": form})

def panel_profesor(request):
    #Verificamos si la variable de autenticacion existe
    if not request.session.get('autenticado'):
        return redirect('Login_profesor')
    return render(request, 'Panel_profesor.html')

def logout_profesor(request):
    request.session.pop('autenticado',None)
    return redirect('login_profesor')

#cambios en este metodo enfocado en las notas, falta testeo 
def agregar_calificacion(request):
    if request.method == 'POST':
        form = CalificacionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/Panel_profesor')  # Redirige a la vista deseada
    else:
        form = CalificacionForm()

    return render(request, 'Agregar_calificacion.html', {'form': form})
