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

    class Meta:
        managed = False
        db_table = 'appproject_estudiante'
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



class Calificacion(models.Model):
    idCalificacion = models.AutoField(primary_key=True)
    nota = models.DecimalField(max_digits=5, decimal_places=1)
    fecha_registro = models.DateField()
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE)
    clase = models.ForeignKey(Clases, on_delete=models.CASCADE, default=10)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nota} - {self.estudiante.nombre} {self.estudiante.apellido}"
    
    
class Administrador(models.Model):
    idAdministrador = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45)
    apellido = models.CharField(max_length=45)
    correo = models.EmailField(max_length=45)
    rut = models.CharField(max_length=45)
    contraseña = models.CharField(max_length=45)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
