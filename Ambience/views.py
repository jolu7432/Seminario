from datetime import timedelta
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, render

# Create your views here.
from django.template import RequestContext
from django.utils import timezone
from django.utils.datetime_safe import datetime
from django.views.decorators.csrf import csrf_exempt
from Ambience.models import Sensor, Silo, Puesto, Alerta
from ipware.ip import get_ip


@csrf_exempt
def index(request):
    return render_to_response('index.html', context_instance=RequestContext(request))


@login_required(login_url="index")
@csrf_exempt
def principal(request):
    s = []
    if request.user.es_operario:
        puestos = Puesto.objects.filter(user=request.user)
        for p in puestos:
            s.append(p.silo)
    else:
        s = Silo.objects.filter(empresa=request.user.empresa)
    return render_to_response('principal.html', {'silos': s},
                              context_instance=RequestContext(request))


@login_required(login_url="index")
@csrf_exempt
def statistics(request):
    if not request.user.es_operario:
        s = Silo.objects.filter(empresa=request.user.empresa)
        return render_to_response('statistics.html', {'silos': s},
                                  context_instance=RequestContext(request))
    else:
        msg = "No tienes Permiso."
        return render_to_response('error.html', {'error': msg}, context_instance=RequestContext(request))


@login_required(login_url="index")
@csrf_exempt
def contact(request):
    return render_to_response('contact.html', context_instance=RequestContext(request))


@login_required(login_url="index")
@csrf_exempt
def abm(request):
    if not request.user.es_operario:
        if request.method == 'POST':
            op = False
            if 'operario' in request.POST:
                op = True
            user = User.objects.create_user(username=request.POST['usuario'], password=request.POST['password'],
                                            email=request.POST['email'], first_name=request.POST['nombre'],
                                            last_name=request.POST['apellido'],
                                            es_operario=op, empresa=request.user.empresa)
            user.save()
            silos = request.POST.getlist('silo')
            for s in silos:
                pues = Puesto()
                pues.user = user
                pues.silo = Silo.objects.get(id=s)
                pues.save()
            return render_to_response('principal.html', context_instance=RequestContext(request))
        return render_to_response('abm.html', {'usuarios': User.objects.all(), 'puestos': Puesto.objects.all(),
                                               'silos': Silo.objects.filter(empresa=request.user.empresa)},
                                  context_instance=RequestContext(request))
    else:
        msg = "No tienes Permiso."
        return render_to_response('error.html', {'error': msg}, context_instance=RequestContext(request))


@csrf_exempt
def facebook(request):
    return render_to_response('https://www.facebook.com.ar', context_instance=RequestContext(request))


@csrf_exempt
def twiter(request):
    return render_to_response('https://www.twiter.com', context_instance=RequestContext(request))


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
                if user.is_staff:
                    return HttpResponseRedirect('admin')
                return HttpResponseRedirect(reverse('principal'))
            else:
                error = 'Cuenta desactivada. Pongase en contacto con el administrador del sitio.'
                return render_to_response('index.html', {'error': error})
        else:
            error = 'Usuario y/o clave incorrecta'
            return render_to_response('index.html', {'error': error})
    else:
        return render_to_response('index.html', {'error': error})


@csrf_exempt
def logout_user(request):
    logout(request)
    return render_to_response('index.html')


@csrf_exempt
def sendEmail(request):
    return render_to_response('principal.html', context_instance=RequestContext(request))


def server(request):
    msg = ""
    if 'token' in request.GET and request.GET['token'] == "1234":
        ip = get_ip(request)
        if ip is not None and Silo.objects.filter(ip_asignada=ip).exists():
            si = Silo.objects.get(ip_asignada=ip)
            queryset = Sensor.objects.filter(silo=si)
            fecha = datetime.today()
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
            if request.GET['alerta'] == "1":
                email(request)
                # enviar email
            msg = "Guardado Correcto."
        else:
            msg = "Ip no alojada en la base de datos."
    else:
        msg = "Token incorrecto."
    return render_to_response('error.html', {'error': msg}, context_instance=RequestContext(request))


def email(request):
    # msg = ""
    # if 'token' in request.GET and request.GET['token'] == "1234":
    #     ip = get_ip(request)
    #     if ip is not None and Silo.objects.filter(ip_asignada=ip).exists():
    email = EmailMessage("Se produjo alerta en Arduino",
                         "Se ha producido un alerta en el silo ... sensor... Detalle de Sensores:",
                         to=['jorgeluis168@hotmail.com'])
    email.send()
    # msg = "Envio Correcto"
    # else:
    #     msg = "Ip no alojada en la base de datos."
    # else:
    #     msg = "Token incorrecto."
    # return render_to_response('error.html', {'error': msg}, context_instance=RequestContext(request))


@csrf_exempt
def traerSilo(request):
    usuario = User.objects.get(id=request.POST['idUser'])
    silos = []
    if usuario.es_operario:
        puestos = Puesto.objects.filter(user=usuario)
        for p in puestos:
            silos.append(p.silo)
    else:
        silos = Silo.objects.filter(empresa=usuario.empresa)
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
            Alerta.objects.filter(es_alerta=True, sensor__silo=sil, tiempo__range=[fechaD, fechaH]).order_by('-tiempo'))
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

    # sensores = list(Sensor.objects.filter(silo=sil))
    # sen = []
    # for s in sensores:
    #     obj = Sensor()
    #     obj.nombre = s.nombre
    #     obj.humedad = s.humedad
    #     obj.silo = s.silo
    #     obj.temperatura = s.temperatura
    #     obj.tiempo = s.tiempo.date()
    #
    data = []
    # data = serializers.serialize('json', sen)
    # return HttpResponse(data)
    # tiempo = []
    # nombresSensor = []
    # viewModel = Highchart()
    # viewModel.series = []
    # for s in sensores:
    #     if s.nombre not in nombresSensor:
    #         nombresSensor.append(s.nombre)
    #
    # nombre = ''
    # for n in nombresSensor:
    #     queryset = list(querysetPrin.filter(nombre=n))
    #     sen = []
    #     for s in queryset:
    #         if s.tiempo.date() not in tiempo:
    #             tiempo.append(s.tiempo.date())
    #             sen.append(s)
    #             nombre = s.nombre
    #         else:
    #             if s.nombre != nombre:
    #                 sen.append(s)
    #
    #     item = HighchartSeries()
    #     item.name = sen[0].nombre
    #     # for aux in sen:
    #     item.data.append(sen[0].temperatura)
    #     viewModel.series.append(item)
    # viewModel.categories = tiempo
    # data = []
    # data = serializers.serialize('json', viewModel)
    # # return HttpResponse(data)
    #
    # return render(request, 'statistics.html', {'responses': json.dumps(data)})


def data(request):
    return Sensor.objects.all()
