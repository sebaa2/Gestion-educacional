from django.db import models


class Profesor(models.Model):
    idProfesor = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45)
    apellido = models.CharField(max_length=45)
    telefono = models.IntegerField()
    correo = models.EmailField(max_length=45)
    rut = models.CharField(max_length=45)
    contraseña = models.CharField(max_length=45)
    matricula = models.DateField()


    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Clases(models.Model):
    idClases = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45)
    fecha_matricula = models.DateField()
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre


class Curso(models.Model):
    idCurso = models.AutoField(primary_key=True)
    nombre_curso = models.CharField(max_length=45)
    clases = models.ManyToManyField(Clases)
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE, related_name='cursos')
    def __str__(self):
        return self.nombre_curso

class Estudiante(models.Model):
    idEstudiante = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45)
    apellido = models.CharField(max_length=45)
    fecha_nacimiento = models.DateField()
    direccion = models.CharField(max_length=45)
    telefono = models.IntegerField()
    matricula = models.DateField()
    rut = models.IntegerField()
    contraseña = models.CharField(max_length=200)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, default='Sin asignar')

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Asistencia(models.Model):
    idAsistencia = models.AutoField(primary_key=True)
    fecha = models.DateField()
    presente = models.BooleanField(default=False)
    no_presente = models.BooleanField(default=False)
    estudiante = models.ForeignKey('Estudiante', on_delete=models.CASCADE)
    curso = models.ForeignKey('Curso', on_delete=models.CASCADE, null=True)
    clase = models.ForeignKey('Clases', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.estudiante} - {self.fecha} - Presente: {self.presente}"
    
class Administrador(models.Model):
    idAdministrador = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45)
    apellido = models.CharField(max_length=45)
    correo = models.EmailField(max_length=45)
    rut = models.CharField(max_length=45)
    contraseña = models.CharField(max_length=45)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Documento(models.Model):
    titulo = models.CharField(max_length=100)
    archivo = models.FileField(upload_to='documentos/')  # Almacena el archivo en la carpeta 'documentos'
    descripcion = models.TextField(null=True, blank=True)  # Descripción opcional del archivo
    fecha_subida = models.DateField(auto_now_add=True)
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE)  # El documento será subido por un profesor
    clase = models.ForeignKey(Clases, on_delete=models.CASCADE, null=True, blank=True)  # Relacionado con una clase, si lo deseas
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, null=True, blank=True)  # Relacionado con un curso, si lo deseas

    def __str__(self):
        return f"Documento {self.titulo} - {self.profesor.nombre}"

class Tarea(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_entrega = models.DateField()
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='tareas')
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE, related_name='tareas')
    clase = models.ForeignKey(Clases, on_delete=models.CASCADE, related_name='tareas')

    def __str__(self):
        return self.titulo

class Prueba(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    documento = models.FileField(upload_to='pruebas/')  # Almacena el archivo en la carpeta 'pruebas'
    fecha = models.DateField()  # Fecha en que se aplicará la prueba
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='pruebas')  # Relaciona la prueba con un curso
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE, related_name='pruebas')  # Relaciona la prueba con un profesor
    clase = models.ForeignKey(Clases, on_delete=models.CASCADE, related_name='pruebas')  # Relaciona la prueba con una asignatura

    def __str__(self):
        return f"Prueba: {self.titulo} - {self.curso.nombre_curso} - {self.profesor.nombre}"

class Calificacion(models.Model):
    idCalificacion = models.AutoField(primary_key=True)
    nota = models.DecimalField(max_digits=5, decimal_places=1)
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE)
    clase = models.ForeignKey(Clases, on_delete=models.CASCADE, default=10)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    prueba = models.ForeignKey(Prueba, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nota} - {self.estudiante.nombre} {self.estudiante.apellido}"
    
class PruebaSubida(models.Model):
    estudiante = models.ForeignKey('Estudiante', on_delete=models.CASCADE)
    prueba = models.ForeignKey(Prueba, on_delete=models.CASCADE)
    archivo = models.FileField(upload_to='pruebas_subidas/')
    fecha_subida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.estudiante} - {self.prueba.titulo}"

class Horario(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    dia = models.CharField(max_length=20, choices=[('Lunes', 'Lunes'), ('Martes', 'Martes'), 
                                                   ('Miércoles', 'Miércoles'), ('Jueves', 'Jueves'), 
                                                   ('Viernes', 'Viernes')])
    jornada = models.CharField(max_length=20, choices=[
        ('Primera Jornada', 'Primera Jornada'),
        ('Segunda Jornada', 'Segunda Jornada'),
        ('Tercera Jornada', 'Tercera Jornada'),
    ])
    clase = models.ForeignKey(Clases, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.curso.nombre_curso} - {self.dia} - {self.jornada} - {self.clase.nombre}"

