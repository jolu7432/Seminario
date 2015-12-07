# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Alerta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('temperatura', models.FloatField(null=True, blank=True)),
                ('humedad', models.FloatField(null=True, blank=True)),
                ('es_alerta', models.BooleanField()),
                ('tiempo', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=100)),
                ('direccion', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Puesto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Silo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip_asignada', models.CharField(max_length=20)),
                ('ubicacion', models.CharField(max_length=100)),
                ('empresa', models.ForeignKey(to='Ambience.Empresa')),
            ],
        ),
        migrations.AddField(
            model_name='sensor',
            name='silo',
            field=models.ForeignKey(to='Ambience.Silo'),
        ),
        migrations.AddField(
            model_name='puesto',
            name='silo',
            field=models.ForeignKey(to='Ambience.Silo'),
        ),
        migrations.AddField(
            model_name='puesto',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='alerta',
            name='sensor',
            field=models.ForeignKey(to='Ambience.Sensor'),
        ),
    ]
