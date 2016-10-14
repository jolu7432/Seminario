from datetime import timedelta
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.template import RequestContext
from django.utils.datetime_safe import datetime
from django.views.decorators.csrf import csrf_exempt
from Ambience.models import Sensor, Silo, Puesto, Alerta
from ipware.ip import get_ip
import pdb

@csrf_exempt
def index(request):
    return render(request, 'index.html')


@login_required(login_url="index")
@csrf_exempt
def principal(request):
    silos = []
    if request.user.is_superuser:
        silos = Silo.objects.all()
    else:
        if request.user.is_staff:
            silos = Silo.objects.filter(empresa=request.user.userprofile.empresa)           
        else:   
            puestos = Puesto.objects.filter(user=request.user)
            for p in puestos:
                silos.append(p.silo)   
    return render(request, 'principal.html', {'silos': silos})


@login_required(login_url="index")
@csrf_exempt
def statistics(request):
    if request.user.is_superuser:
        silos = Silo.objects.all()
    else:
        if request.user.is_staff:           
            silos = Silo.objects.filter(empresa=request.user.userprofile.empresa)           
        else:
            msg = "No tienes Permiso."
            return render(request, 'error.html', {'error': msg})
    return render(request, 'statistics.html', {'silos': silos})


@login_required(login_url="index")
@csrf_exempt
def contact(request):
    return render(request, 'contact.html')


@login_required(login_url="index")
@csrf_exempt
def abm(request):	   
	if request.user.is_superuser or request.user.is_staff:
		#pdb.set_trace()
		if request.method == 'POST':			  
			if request.POST['usuarioHidden'] == "":
				user = User.objects.create_user(username=request.POST['usuario'], password=request.POST['password'],
				    email=request.POST['email'], first_name=request.POST['nombre'],
				    last_name=request.POST['apellido'],is_staff=False)
				userProfile = UserProfile()
				userProfile.user = user
				userProfile.empresa = request.user.userprofile.empresa                
				userProfile.save()
			else:
				idUser = request.POST['usuarioHidden']
				user = User.objects.get(id=idUser)
				user.username = request.POST['usuario']
				user.first_name = request.POST['nombre']
				user.email = request.POST['email']
				user.last_name = request.POST['apellido']
			if request.POST['password'] != "":
				user.set_password(request.POST['password'])

			user.save()
			silosAdd = request.POST.getlist('silo')
			puestosAsignados = list(Puesto.objects.filter(user=user))

			for s in silosAdd:
				sil = Silo.objects.get(id=s)
				if not existe_silo(request, sil, puestosAsignados):
					pues = Puesto()
					pues.user = user
					pues.silo = sil
					pues.save()
				else:
					eliminar_por_silo(request, sil, puestosAsignados)

			if puestosAsignados.__len__() > 0:
				for p in puestosAsignados:
					Puesto.objects.get(id=p.id).delete() 

			return HttpResponseRedirect('abm')

		if request.user.is_superuser:
			usuarios = User.objects.all()
			silos = Silo.objects.all()
		else:
		    usuarios = User.objects.exclude(is_superuser=True).filter(userprofile__empresa=request.user.userprofile.empresa)
		    silos = Silo.objects.filter(empresa=request.user.userprofile.empresa)     
		return render(request, 'abm.html', {'usuarios': usuarios, 'puestos': Puesto.objects.all(),
		                                       'silos': silos})
	else:
		msg = "No tienes Permiso."
		return render(request, 'error.html', {'error': msg})


def eliminar_por_silo(request, dat, datos):
    for b in datos:
        if b.silo == dat:
            datos.remove(b)


def existe_silo(request, dat, datos):
    resp = False
    for d in datos:
        if d.silo == dat:
            resp = True
    return resp


@csrf_exempt
def facebook(request):
    return render(request, 'https://www.facebook.com.ar')


@csrf_exempt
def twiter(request):
    return render(request, 'https://www.twiter.com')


@csrf_exempt
def login_user(request):
    error = ''
    if request.method == 'POST':
        username = request.POST['user']
        password = request.POST['pass']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                if user.is_superuser:
                    return HttpResponseRedirect('admin')
                return HttpResponseRedirect(reverse('principal'))
            else:
                error = 'Cuenta desactivada. Pongase en contacto con el administrador del sitio.'
                return render(request, 'index.html', {'error': error})
        else:
            error = 'Usuario y/o clave incorrecta'
            return render(request, 'index.html', {'error': error})
    else:
        return render(request, 'index.html', {'error': error})


@csrf_exempt
def logout_user(request):
    logout(request)
    return render(request, 'index.html')


@csrf_exempt
def sendEmail(request):
    try:
        email = EmailMessage("Solicitud de Contacto del Usuario " + request.POST['email'],
                             "Nombre: " + request.POST['nombre'] + " Mensaje: " + request.POST[
                                 'mensaje'] + " Telefono: " +
                             request.POST[
                                 'telefono'],
                             to=['ambiancesa@gmail.com'])
        email.send()
        return render(request, 'contact.html', {'msg': "Envio correcto"})
    except:
        return render(request, 'error.html', {'error': "Error en la conexion con el servidor."})


def server(request):
    msg = ""
    if 'token' in request.GET and request.GET['token'] == "1234":
        ip = get_ip(request)
        if ip is not None and Silo.objects.filter(ip_asignada=ip).exists():
            si = Silo.objects.get(ip_asignada=ip)
            queryset = Sensor.objects.filter(silo=si)
            fecha = datetime.today()
            datos = ""
            for item in queryset:
                i = item.identificador
                alerta = Alerta()
                alerta.tiempo = fecha
                if 't' + `i` in request.GET and request.GET['t' + `i`] is not None:
                    alerta.temperatura = float(request.GET['t' + `i`])
                else:
                    alerta.temperatura = 0
                if 'h' + `i` in request.GET and request.GET['h' + `i`] is not None:
                    alerta.humedad = float(request.GET['h' + `i`])
                else:
                    alerta.humedad = 0
                alerta.sensor = item
                if request.GET['alerta'] == "0":
                    alerta.es_alerta = False
                else:
                    alerta.es_alerta = True
                alerta.save()
                datos += 't' + `i` + "= " + `alerta.temperatura`
                datos += ' h' + `i` + "= " + `alerta.humedad` + " "
            if request.GET['alerta'] == "1":
                to = Puesto.objects.filter(silo=si)
                for t in to:
                    email = EmailMessage("Se produjo alerta en Arduino",
                                         "Se ha producido un alerta en el Silo: Ip=" + si.ip_asignada + ". Ubicacion= " + si.ubicacion + ". Datos Sensores: " + datos,
                                         to=[t.user.email])
                    email.send()
            msg = "Guardado Correcto."
        else:
            msg = "Ip no alojada en la base de datos."
    else:
        msg = "Token incorrecto."
    return render(request,'errorArduino.html', {'error': msg})


@csrf_exempt
def traerSilo(request):
    usuario = User.objects.get(id=request.POST['idUser'])
    silos = []
    if not usuario.is_staff:
        puestos = Puesto.objects.filter(user=usuario)
        for p in puestos:
            silos.append(p.silo)
    else:
        silos = Silo.objects.filter(empresa=usuario.userprofile.empresa)
    data = serializers.serialize('json', silos)
    return HttpResponse(data)


@csrf_exempt
def graficarDash(request):
    sil = Silo.objects.get(ip_asignada=request.POST['silo'])
    fechaD = request.POST['fechaDesde']
    fechaH = request.POST['fechaHasta']
    queryset = []
    if request.POST['consulta'] == "alerta":
        queryset = list(
            Alerta.objects.filter(es_alerta=True,
                                  sensor__silo=sil, tiempo__range=[fechaD, fechaH]).order_by('-tiempo'))
    else:
        queryset = list(
            Alerta.objects.filter(es_alerta=False, sensor__silo=sil, tiempo__range=[fechaD, fechaH]).order_by(
                '-tiempo'))
    respuesta = []
    for item in queryset:
        obj = Alerta()
        obj.es_alerta = item.es_alerta
        obj.humedad = item.humedad
        obj.temperatura = item.temperatura
        item.sensor.id = item.sensor.identificador
        obj.sensor = item.sensor
        t = item.tiempo - timedelta(hours=3)
        obj.tiempo = t.replace(t.year, t.month, t.day, t.hour, t.minute, 0, 0, None)
        respuesta.append(obj)
    data = []
    data = serializers.serialize('json', respuesta)
    return HttpResponse(data)


@csrf_exempt
def borrarUsuario(request):
    User.objects.get(id=request.POST['idUser']).delete()


@csrf_exempt
def traerSensores(request):
    sil = Silo.objects.get(id=request.POST['idSilo'])
    return HttpResponse(serializers.serialize('json', Sensor.objects.filter(silo=sil)))
