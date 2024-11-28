# Generated by Django 5.1 on 2024-11-07 18:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Administrador',
            fields=[
                ('idAdministrador', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=45)),
                ('apellido', models.CharField(max_length=45)),
                ('correo', models.EmailField(max_length=45)),
                ('rut', models.CharField(max_length=45)),
                ('contrasena', models.CharField(max_length=45)),
            ],
        ),
        migrations.CreateModel(
            name='Clases',
            fields=[
                ('idClases', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=45)),
                ('fecha_matricula', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Profesor',
            fields=[
                ('idProfesor', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=45)),
                ('apellido', models.CharField(max_length=45)),
                ('telefono', models.IntegerField()),
                ('correo', models.EmailField(max_length=45)),
                ('rut', models.CharField(max_length=45)),
                ('contrasena', models.CharField(max_length=45)),
                ('matricula', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('idCurso', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_curso', models.CharField(max_length=45)),
                ('clases', models.ManyToManyField(to='appproject.clases')),
            ],
        ),
        migrations.CreateModel(
            name='Estudiante',
            fields=[
                ('idEstudiante', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=45)),
                ('apellido', models.CharField(max_length=45)),
                ('fecha_nacimiento', models.DateField()),
                ('direccion', models.CharField(max_length=45)),
                ('telefono', models.IntegerField()),
                ('matricula', models.DateField()),
                ('rut', models.IntegerField()),
                ('contrasena', models.CharField(max_length=200)),
                ('curso', models.ForeignKey(default='Sin asignar', on_delete=django.db.models.deletion.CASCADE, to='appproject.curso')),
            ],
        ),
        migrations.CreateModel(
            name='Asistencia',
            fields=[
                ('idAsistencia', models.AutoField(primary_key=True, serialize=False)),
                ('fecha', models.DateField()),
                ('presente', models.BooleanField(default=False)),
                ('no_presente', models.BooleanField(default=False)),
                ('clase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appproject.clases')),
                ('curso', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='appproject.curso')),
                ('estudiante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appproject.estudiante')),
            ],
        ),
        migrations.AddField(
            model_name='clases',
            name='profesor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appproject.profesor'),
        ),
        migrations.CreateModel(
            name='Calificacion',
            fields=[
                ('idCalificacion', models.AutoField(primary_key=True, serialize=False)),
                ('nota', models.DecimalField(decimal_places=1, max_digits=5)),
                ('fecha_registro', models.DateField()),
                ('clase', models.ForeignKey(default=10, on_delete=django.db.models.deletion.CASCADE, to='appproject.clases')),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appproject.curso')),
                ('estudiante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appproject.estudiante')),
                ('profesor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appproject.profesor')),
            ],
        ),
    ]
