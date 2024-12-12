from django import forms
from django.core.exceptions import ValidationError
from .models import Estudiante, Profesor, Curso, Clases, Calificacion, Documento, Tarea

class TareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ['titulo', 'descripcion', 'fecha_entrega', 'curso', 'clase']
        widgets = {
            'fecha_entrega': forms.DateInput(attrs={'type': 'date'}),
        }

class LoginForm(forms.Form):
    username  = forms.CharField()
    password =forms.CharField(widget = forms.PasswordInput)

class CalificacionForm(forms.ModelForm):
    class Meta:
        model = Calificacion
        fields = ['nota', 'fecha_registro', 'estudiante', 'curso']
        labels = {
            'fecha_registro': 'Fecha de registro: '
        }
        widgets = {
            'fecha_registro': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
        }
        
class AgregarEstudiantes(forms.ModelForm):
    class Meta:  # Definir la clase Meta para vincular el modelo
        model = Estudiante
        fields = [ 
            "nombre", "apellido", "fecha_nacimiento", 
            "direccion", "telefono", "matricula", 
            "rut", "contraseña", "curso"
        ]  # Definir los campos a usar

        labels = {
            "nombre": 'Nombre ',
            "apellido": 'Apellidos ',
            "fecha_nacimiento": 'Fecha nacimiento ',
            "direccion": 'Dirección ',
            "telefono": 'Teléfono ',
            "matricula": 'Matrícula ',
            "rut": 'Rut ',
            "contraseña": 'Contraseña ',
            "curso": 'Curso '
        }
        
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'matricula': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'rut': forms.TextInput(attrs={'class': 'form-control'}),
            'contraseña': forms.PasswordInput(attrs={'class': 'form-control'}),
            'curso': forms.Select(attrs={'class': 'form-control'}),  # Menú desplegable para curso
        }

class AgregarProfesor(forms.ModelForm):
    curso = forms.ModelMultipleChoiceField(
        queryset=Curso.objects.all(), 
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Profesor
        fields = ['nombre', 'apellido', 'telefono', 'correo', 'rut', 'contraseña', 'matricula']
        labels = {
            'nombre': 'Nombre',
            'apellido': 'Apellido',
            'telefono': 'Teléfono',
            'correo': 'Correo Electrónico',
            'rut': 'RUT',
            'contraseña': 'Contraseña',
            'matricula': 'fecha de Contrato',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.NumberInput(attrs={'class': 'form-control'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control'}),
            'rut': forms.TextInput(attrs={'class': 'form-control'}),
            'contraseña': forms.PasswordInput(attrs={'class': 'form-control'}),
            'matricula': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def clean_curso(self):
        cursos = self.cleaned_data.get('curso')
        
        # Si no hay cursos seleccionados, retorna la lista vacía
        if not cursos:
            return cursos

        # Verificar que ningún curso ya tenga un profesor asignado
        for curso in cursos:
            if curso.profesor_set.exists():
                raise ValidationError(f"El curso {curso.nombre_curso} ya tiene un profesor asignado.")
        
        return cursos

class AgregarCursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ['nombre_curso', 'clases']  # Incluye el campo ManyToMany

        labels = {
            'nombre_curso': 'Nombre del Curso',
            'clases': 'Clases',
        }
        
        widgets = {
            'nombre_curso': forms.TextInput(attrs={'class': 'form-control'}),
            'clases': forms.CheckboxSelectMultiple(),  # Muestra las clases como una lista de checkboxes
        }
    def clean_nombre_curso(self):
        # Obtener el nombre del curso y convertirlo a minúsculas para comparación insensible a mayúsculas
        nombre_curso = self.cleaned_data['nombre_curso'].lower()
        
        # Verificar si ya existe un curso con este nombre (ignorando mayúsculas/minúsculas)
        cursos_existentes = Curso.objects.filter(nombre_curso__iexact=nombre_curso)
        
        # Si es un formulario de edición, excluir el curso actual de la verificación
        if self.instance.pk:
            cursos_existentes = cursos_existentes.exclude(pk=self.instance.pk)
        
        # Si existe un curso con el mismo nombre, lanzar un error de validación
        if cursos_existentes.exists():
            raise ValidationError("Ya existe un curso con este nombre.")
        
        return nombre_curso

class AgregarAsignaturas(forms.ModelForm):
    class Meta:
        model = Clases
        fields = ['nombre', 'fecha_matricula', 'profesor', 'hora_entrada', 'hora_salida', 'fecha_horario']
        labels = {
            'nombre': 'Nombre asignatura',
            'fecha_matricula': 'Fecha inscripción',
            'profesor': 'Profesor',
            'hora_entrada': 'Hora entrada',
            'hora_salida': 'Hora salida',
            'fecha_horario': 'Fecha horario'
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_matricula': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'profesor': forms.Select(attrs={'class': 'form-control'}),
            'hora_entrada': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'hora_salida': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'fecha_horario': forms.CheckboxSelectMultiple(),
        }
    def clean_nombre(self):
        # Obtener el nombre de la asignatura y convertirlo a minúsculas para comparación insensible a mayúsculas
        nombre = self.cleaned_data['nombre'].lower()
        
        # Verificar si ya existe una asignatura con este nombre (ignorando mayúsculas/minúsculas)
        clases_existentes = Clases.objects.filter(nombre__iexact=nombre)
        
        # Si es un formulario de edición, excluir la clase actual de la verificación
        if self.instance.pk:
            clases_existentes = clases_existentes.exclude(pk=self.instance.pk)
        
        # Si existe una asignatura con el mismo nombre, lanzar un error de validación
        if clases_existentes.exists():
            raise ValidationError("Ya existe una asignatura con este nombre.")
        
        return nombre

class DocumentoForm(forms.ModelForm):
    class Meta:
        model = Documento
        fields = ['titulo', 'archivo', 'descripcion', 'clase', 'curso']