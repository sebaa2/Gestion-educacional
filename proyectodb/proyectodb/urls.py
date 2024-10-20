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
from profesorapp.views import login_profesor, panel_profesor, agregar_calificacion, logout_profesor
from adminapp.views import login_admin, panel_administrador, logout_admin, Registrar_estudiantesForm, Registrar_profesorForm, lista_profesores, agregar_curso, lista_cursos, agregar_asignatura, lista_asignaturas, lista_estudiantes, Eliminar_estudiantes, Eliminar_profesor, Eliminar_curso, Eliminar_asignatura
from appproject.views import Principal, login_view, panel_estudiantes, logout, panel_asignaturas_estudiante

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Principal, name="principal"),
    #acciones del estudiantes
    path('Login_estudiante/', login_view, name="login_estudiantes"),
    path('logout_estudiantes/',logout,name="logout_estudiantes"),
    path('Panel_estudiantes/', panel_estudiantes, name="panel_estudiantes"),
    path('panel_estudiantes/<int:idEstudiante>/asignaturas/', panel_asignaturas_estudiante, name='panel_asignaturas_estudiante'),
    #acciones del admin
    path('Login_admin/', login_admin, name="Login_admin"),
    path('Panel_admin/', panel_administrador, name="Panel_admin"),
    path('logout_admin/', logout_admin, name="logout_admin"),
    path('Lista_asignaturas/', lista_asignaturas, name="lista_asignaturas"),
    path('lista_cursos/', lista_cursos, name='lista_cursos'),
    path('agregar_asignatura/', agregar_asignatura, name='agregar_asignatura'),
    path('agregar_curso/', agregar_curso, name='agregar_curso'),
    path('agregar_estudiante/', Registrar_estudiantesForm, name='agregar_estudiante'),
    path('agregar_profesor/', Registrar_profesorForm, name='agregar_profesor'),
    path('Lista_estudiantes/', lista_estudiantes, name="lista_estudiantes"),
    path('Lista_profesores/', lista_profesores, name='Lista_profesores'),
    path('Lista_profesores/EliminarProfesor/<int:idProfesor>', Eliminar_profesor, name="eliminar_profesor"),
    path('Lista_estudiantes/EliminarEstudiante/<int:idEstudiante>', Eliminar_estudiantes, name="eliminar_estudiantes"),
    path('lista_cursos/EliminarCurso/<int:idCurso>', Eliminar_curso, name="eliminar_curso"),
    path('Lista_asignaturas/EliminarAsignatura/<int:idClases>', Eliminar_asignatura, name="eliminar_asignaturas"),
    #acciones del profesor
    path('Login_profesor/', login_profesor, name='login_profesor'),
    path('Logout_profesor/', logout_profesor, name='logout_profesor'),
    path('Panel_profesor/', panel_profesor, name='panel_profesor'),
    path('Agregar_calificacion/', agregar_calificacion, name="agregar_calificacion")

]
