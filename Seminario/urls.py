"""Seminario URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.views.debug import default_urlconf
from django.views.generic import RedirectView
from Ambience import views as Ambience

urlpatterns = [
    url(r'^admin', include(admin.site.urls)),
    url(r'^$', Ambience.index, name='index'),
    url(r'^principal$', Ambience.principal, name='principal'),
    url(r'^logIn$', Ambience.login_user, name='logIn'),
    url(r'^logOut$', Ambience.logout_user, name='logOut'),
    url(r'^statistics$', Ambience.statistics, name='statistics'),
    url(r'^contact$', Ambience.contact, name='contact'),   
    url(r'^abm$', Ambience.abm, name='abm'),
    url(r'^sendEmail$', Ambience.sendEmail, name='sendEmail'),
    url(r'^server', Ambience.server, name='server'),
    url(r'^traerSilo', Ambience.traerSilo, name='traerSilo'),
    url(r'^graficarDash', Ambience.graficarDash, name='graficarDash'),
    url(r'^borrarUsuario', Ambience.borrarUsuario, name='borrarUsuario'),
    url(r'^traerSensores', Ambience.traerSensores, name='traerSensores'),

]
