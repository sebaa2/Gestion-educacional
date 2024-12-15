from django import forms
from django.core.exceptions import ValidationError
from .models import Estudiante, Profesor, Curso, Clases, Calificacion, Documento, Tarea, Prueba, PruebaSubida, Horario

class PruebaForm(forms.ModelForm):
    class Meta:
        model = Prueba
        fields = ['titulo', 'descripcion', 'documento', 'fecha', 'curso', 'clase']

    def __init__(self, *args, **kwargs):
        profesor_id = kwargs.pop('profesor_id', None)  # Tomar el ID del profesor desde la sesión
        super().__init__(*args, **kwargs)

        if profesor_id:
            # Filtrar los cursos asociados al profesor autenticado
            self.fields['curso'].queryset = Curso.objects.filter(profesor_id=profesor_id).distinct()

            # Filtrar las clases asociadas al profesor autenticado
            self.fields['clase'].queryset = Clases.objects.filter(profesor_id=profesor_id)



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
    curso = forms.ModelChoiceField(
        queryset=Curso.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
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
        fields = ['nombre', 'fecha_matricula', 'profesor', 'fecha_horario']
        fields = ['nombre', 'fecha_matricula', 'profesor']
        labels = {
            'nombre': 'Nombre asignatura',
            'fecha_matricula': 'Fecha inscripción',
            'profesor': 'Profesor',
            'fecha_horario': 'Fecha horario'
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_matricula': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'profesor': forms.Select(attrs={'class': 'form-control'}),
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
    
    def __init__(self, *args, **kwargs):
        profesor_id = kwargs.pop('profesor_id', None)
        super().__init__(*args, **kwargs)
        if profesor_id:
            # Filter courses to only those with classes taught by this professor
            self.fields['curso'].queryset = Curso.objects.filter(clases__profesor_id=profesor_id).distinct()
            # Filter classes to only those taught by this professor
            self.fields['clase'].queryset = Clases.objects.filter(profesor_id=profesor_id)

    class Meta:
        model = Documento
        fields = ['titulo', 'archivo', 'descripcion', 'clase', 'curso']

class FiltroNotasForm(forms.Form):
    curso = forms.ModelChoiceField(queryset=Curso.objects.none(), label="Curso")
    clase = forms.ModelChoiceField(queryset=Clases.objects.none(), label="Clase")
    prueba = forms.ModelChoiceField(queryset=Prueba.objects.none(), label="Prueba")

    def __init__(self, *args, **kwargs):
        profesor_id = kwargs.pop('profesor_id', None)  # Extraer profesor_id
        super().__init__(*args, **kwargs)
        if profesor_id:
            self.fields['curso'].queryset = Curso.objects.filter(profesor=profesor_id).distinct()
            self.fields['clase'].queryset = Clases.objects.filter(profesor=profesor_id).distinct()
            self.fields['prueba'].queryset = Prueba.objects.filter(profesor=profesor_id).distinct()
        else:
            self.fields['curso'].queryset = Curso.objects.all()
            self.fields['clase'].queryset = Clases.objects.all()
            self.fields['prueba'].queryset = Prueba.objects.all()

class PruebaSubidaForm(forms.ModelForm):
    class Meta:
        model = PruebaSubida
        fields = ['archivo']

class HorarioForm(forms.ModelForm):
    class Meta:
        model = Horario
        fields = ['dia', 'jornada', 'clase']

    # Definir las opciones de días y jornadas
    dia = forms.ChoiceField(choices=[
        ('Lunes', 'Lunes'),
        ('Martes', 'Martes'),
        ('Miércoles', 'Miércoles'),
        ('Jueves', 'Jueves'),
        ('Viernes', 'Viernes'),
    ], label="Día")

    jornada = forms.ChoiceField(choices=[
        ('Primera Jornada', 'Primera Jornada'),
        ('Segunda Jornada', 'Segunda Jornada'),
        ('Tercera Jornada', 'Tercera Jornada'),
    ], label="Jornada")

    clase = forms.ModelChoiceField(queryset=Clases.objects.none(), label="Clase")

    def __init__(self, *args, **kwargs):
        curso = kwargs.pop('curso', None)  # Obtener el curso pasado a través de la vista
        super().__init__(*args, **kwargs)
        if curso:
            # Filtrar las clases por el curso seleccionado
            self.fields['clase'].queryset = Clases.objects.filter(curso=curso)