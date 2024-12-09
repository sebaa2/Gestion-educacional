from django import forms
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
    class Meta:
        model = Profesor
        fields = ['nombre', 'apellido', 'telefono', 'correo', 'rut', 'contraseña', 'matricula']  # Especifica los campos que deseas incluir
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

class DocumentoForm(forms.ModelForm):
    class Meta:
        model = Documento
        fields = ['titulo', 'archivo', 'descripcion', 'clase', 'curso']