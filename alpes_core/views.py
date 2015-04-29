#coding: utf-8

from django.shortcuts import render

from alpes_core.models import Tese
from django.template import RequestContext, loader



# Create your views here.
def home(request):
	
	context = RequestContext(request,{'teses' : Tese.objects.filter(grupo_idgrupo=1064)})
	
	return render(request, 'inicio.html', context)

# def index(request):
#     return render(request,'index.html', {})
# 
# def charts(request):
#     return render(request,'charts.html', {})
# 
# def pages(request):
#     return render(request,'{{request}}.html', {})