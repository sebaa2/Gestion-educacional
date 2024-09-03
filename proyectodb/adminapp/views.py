from django.shortcuts import render
from appproject.models import Administrador
from appproject.forms import LoginForm
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from datetime import datetime

def login_admin(request):
    form = LoginForm(request.POST)
    if request.method =="POST" and form.is_valid(): 
        #Asociamos las variables del formulario a variables de la función
        txt_usuario = form.cleaned_data.get("txt_username")
        txt_password = form.cleaned_data.get("txt_password")
        try:
            user = Administrador.objects.get(rut = txt_usuario)
            #En caso de que la contraseña ingresada sea igual a la contraseña almacenada
            if user.contraseña == txt_password:
                request.session['autenticado'] = True 
                request.session['usuario'] = user.rut 
                request.session['nombre_completo'] = user.nombre +" "+ user.apellido
                #Redireccionamos a lista de gestiones
                return redirect("/Panel_admin")
            else:
                form.add_error(None, 'Contraseña incorrecta')
        except Administrador.DoesNotExist:
            form.add_error(None, 'Usuario no existe')
    return render(request, "Login_admin.html", {"form": form})

def logout_admin(request):
    request.session.pop('autenticado',None)
    return redirect('/Login_admin')

def panel_administrador(request,):
    return render(request, 'Panel_admin.html')