from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from .models import Noticia

def index(request):
    noticias = Noticia.objects.order_by('id')
    template = loader.get_template('raspador/noticias.html')
    context = {
        'noticias': noticias,
    }
    return HttpResponse(template.render(context, request))
