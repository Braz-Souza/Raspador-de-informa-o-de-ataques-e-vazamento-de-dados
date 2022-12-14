from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from .models import Noticia
from .raspador import pesquisar_por_palavra_chaves_e_depois_salvar_noticias;
import time



def index(request):
    agora = time.localtime()
    if agora.tm_hour == 14 and agora.tm_min == 17:
        pesquisar_por_palavra_chaves_e_depois_salvar_noticias(Noticia)
    noticias = Noticia.objects.order_by('id')
    template = loader.get_template('raspador/noticias.html')
    context = {
        'noticias': noticias,
    }
    if (request.GET.get('deletedb')):
        Noticia.objects.all().delete()
    if (request.GET.get('btnraspador')):
        pesquisar_por_palavra_chaves_e_depois_salvar_noticias(Noticia);
    return HttpResponse(template.render(context, request))
