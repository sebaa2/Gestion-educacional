from django.contrib import admin

from .models import Estudiante, Clases, Curso, Calificacion, Profesor, Asistencia, Administrador

admin.site.register(Curso)
admin.site.register(Estudiante)
admin.site.register(Clases)
admin.site.register(Calificacion)
admin.site.register(Profesor)
admin.site.register(Asistencia)
admin.site.register(Administrador)
