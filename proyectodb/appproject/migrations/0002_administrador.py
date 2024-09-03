# Generated by Django 5.1 on 2024-09-03 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appproject', '0001_initial'),
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
                ('contraseña', models.CharField(max_length=45)),
            ],
        ),
    ]
