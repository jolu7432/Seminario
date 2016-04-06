from django.contrib import admin

# Register your models here.
from Ambience.models import *


class SensorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'identificador', 'silo')


class SiloAdmin(admin.ModelAdmin):
    list_display = ('ip_asignada', 'ubicacion', 'empresa')


class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'direccion', 'email')


class AlertaAdmin(admin.ModelAdmin):
    list_display = ('sensor', 'temperatura', 'humedad', 'es_alerta', 'tiempo')

class PuestoAdmin(admin.ModelAdmin):
    list_display = ('user', 'silo')

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'empresa', 'es_operario')

admin.site.register(Empresa, EmpresaAdmin)
admin.site.register(Silo, SiloAdmin)
admin.site.register(Sensor, SensorAdmin)
admin.site.register(Puesto, PuestoAdmin)
admin.site.register(Alerta, AlertaAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.AdminSite.site_url = "/principal"
