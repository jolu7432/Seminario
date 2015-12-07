from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Empresa(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    email = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Silo(models.Model):
    ip_asignada = models.CharField(max_length=20)
    ubicacion = models.CharField(max_length=100)
    empresa = models.ForeignKey(Empresa)

    def __str__(self):
        return self.ip_asignada


class Sensor(models.Model):
    nombre = models.CharField(max_length=100)
    identificador = models.IntegerField()
    silo = models.ForeignKey(Silo)

    def __str__(self):
        return self.nombre


class Alerta(models.Model):
    sensor = models.ForeignKey(Sensor)
    temperatura = models.FloatField(null=True, blank=True)
    humedad = models.FloatField(null=True, blank=True)
    es_alerta = models.BooleanField()
    tiempo = models.DateTimeField()


class Puesto(models.Model):
    user = models.ForeignKey(User)
    silo = models.ForeignKey(Silo)


User.add_to_class('empresa', models.ForeignKey(Empresa, default=1))
User.add_to_class('es_operario', models.BooleanField(default=False))
