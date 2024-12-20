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
from profesorapp.views import login_profesor, panel_profesor, logout_profesor, clases_del_profesor, cursos_del_profesor, listar_calificaciones, Eliminar_calificacion, subir_documento, asignar_tarea, crear_prueba, filtrar_notas, asignar_notas, ver_pruebas_realizadas
from adminapp.views import editar_profesor, login_admin, panel_administrador, logout_admin, Registrar_estudiantesForm, Registrar_profesorForm, lista_profesores, agregar_curso, lista_cursos, agregar_asignatura, lista_asignaturas, lista_estudiantes, Eliminar_estudiantes, Eliminar_profesor, Eliminar_curso, Eliminar_asignatura, editar_estudiante, actualizar_asignatura, actualizar_curso, admin_dashboard, armar_horario, seleccionar_curso, ver_horario
from appproject.views import Principal, login_view, panel_estudiantes, logout, panel_asignaturas_estudiante, calificaciones_estudiante, horario_estudiante, listar_documentos, descargar_documento, ver_tareas, plantilla_accionesprofe, ver_pruebas, subir_prueba, ver_horario_curso

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Principal, name="principal"),
    #acciones del estudiantes
    path('Login_estudiante/', login_view, name="login_estudiantes"),
    path('logout_estudiantes/',logout,name="logout_estudiantes"),
    path('Panel_estudiantes/', panel_estudiantes, name="panel_estudiantes"),
    path('panel_estudiantes/<int:idEstudiante>/asignaturas/', panel_asignaturas_estudiante, name='panel_asignaturas_estudiante'),
    path('mis_calificaciones/', calificaciones_estudiante, name='mis_calificaciones'),
    path('horario_estudiante/<int:estudiante_id>/', horario_estudiante, name='horario_estudiante'),
    path('listar_documentos/', listar_documentos, name='listar_documentos'),
    path('descargar_documento/<int:documento_id>/', descargar_documento, name='descargar_documento'),
    path('tareas/', ver_tareas, name='ver_tareas'),
    path('redirigir/', plantilla_accionesprofe, name="redirigir"),
    path('ver_pruebas/', ver_pruebas, name="ver_pruebas"),
    path('subir-prueba/', subir_prueba, name='subir_prueba'),
    path('ver-horario-curso/<int:curso_id>/', ver_horario_curso, name='ver_horario_curso'),

    #accciones del admin
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
    path('editar_estudiante/<int:idEstudiante>/',editar_estudiante, name='editar_estudiante'),
    path('editar_profesor/<int:idProfesor>/',editar_profesor, name='editar_profesor'),
    path('actualizar-asignatura/<int:id_clase>/', actualizar_asignatura, name='actualizar_asignatura'),
    path('seleccionar-curso/', seleccionar_curso, name='seleccionar_curso'),
    path('armar-horario/', armar_horario, name='armar_horario'),
    path('ver-horario/<int:curso_id>/', ver_horario, name='ver_horario'),
    path('dashboard/', admin_dashboard, name='admin_dashboard'),
    #acciones del profesor
    path('Login_profesor/', login_profesor, name='login_profesor'),
    path('Logout_profesor/', logout_profesor, name='logout_profesor'),
    path('Panel_profesor/', panel_profesor, name='panel_profesor'),
    path('clases_profesor/', clases_del_profesor, name='clases_profesor'),
    path('cursos_profesor/', cursos_del_profesor, name='cursos_profesor'),
    path('listar_calificaciones/', listar_calificaciones, name='listar_calificaciones'),
    path('listar_calificaciones/Eliminarcalificaion/<int:idCalificacion>', Eliminar_calificacion, name='Eliminarcalificacion'),
    path('subir_documento/', subir_documento, name='subir_documento'),
    path('asignar_tarea/', asignar_tarea, name='asignar_tarea'),
    path('actualizar-curso/<int:id_curso>/', actualizar_curso, name='actualizar_curso'),
    path('crear-prueba/', crear_prueba, name='crear_prueba'),
    path('filtrar-notas/', filtrar_notas, name='filtrar_notas'),
    path('asignar-notas/<int:prueba_id>/', asignar_notas, name='asignar_notas'),
    path('ver-pruebas-realizadas/', ver_pruebas_realizadas, name='ver_pruebas_realizadas'),

]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

