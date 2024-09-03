"""
URL configuration for proyectodb project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from adminapp.views import login_admin, panel_administrador, logout_admin
from appproject.views import lista_estudiantes, Agregar_estudiantes, Registrar_estudiantes, Eliminar_estudiantes, Actualizar_estudiantes, Editar_estudiante, Principal, login_view, panel_estudiantes, Asistencias_estudiantes, logout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Principal, name="principal"),
    path('Lista_estudiantes/', lista_estudiantes, name="lista_estudiantes"),
    path('Agregar_estudiantes', Agregar_estudiantes, name="agregar_estudiantes"),
    path('RegistrarEstudiante/', Registrar_estudiantes),
    path('Lista_estudiantes/EliminarEstudiante/<int:idEstudiante>', Eliminar_estudiantes),
    path('Lista_estudiantes/ActualizarEstudiante/<int:idEstudiante>/', Actualizar_estudiantes, name='actualizar_estudiantes'),
    path('Lista_estudiantes/EditarEstudiante/<int:idEstudiante>/', Editar_estudiante, name='editar_estudiante'),
    path('Login_estudiante/', login_view, name="login_estudiantes"),
    path('logout/',logout,name="logout"),
    path('Panel_estudiantes/', panel_estudiantes, name="panel_estudiantes"),
    #panel estudiantes
    path('Asistencia_estudiantes/', Asistencias_estudiantes, name="Asistencia_estudiantes"),
    #panel admin
    path('Login_admin/', login_admin, name="Login_admin"),
    path('Panel_admin/', panel_administrador, name="Panel_admin"),
    path('logout_admin/', logout_admin, name="logout"),
]
