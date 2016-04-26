#coding: utf-8

##################################################################
### CÓDIGO DESENVOLVIDO POR SABRINA SIQUEIRA PANCERI            ##
### PROTÓTIPO DE SUA  DISSERTAÇÃO DE MESTRADO                   ##
### ESSE CÓDIGO PODE SER COPIADO, ALTERADO E DISTRIBUÍDO        ##
### DESDE QUE SUA FONTE SEJA REFERENCIADA                       ##
### PARA MAIS INFORMAÇÕES, ENTRE EM CONTATO ATRAVÉS DO EMAIL    ##
### SABRINASPANCERI@GMAIL.COM                                   ##
##################################################################

from datetime import datetime
import HTMLParser
import re
from django.shortcuts import render
from django.template import RequestContext
from django.db import connection

from alpes_core.models import Tese, Grupo
from alpes_core.clusterArgInicial import clusterArgInicial
from alpes_core.clusterFinal import clusterFinal
from alpes_core.gruposArgumentacao import gruposArgumentacao

from pytagcloud import create_tag_image, make_tags, create_html_data, LAYOUT_HORIZONTAL
from pytagcloud.colors import COLOR_SCHEMES
from pytagcloud.lang.counter import get_tag_counts


import yappi
import time


# Create your views here.
def home(request):
####################################################################################
## 1) COLOCAR DE FORMA OPCIONAL PARA ESCOLHA DO USUÁRIO
## 2) FAZER TELA QUE APRESENTE TODOS OS DEBATES E QUE O USUÁRIO POSSA ESCOLHER 
####################################################################################	
	dados = []	
	
	#context = RequestContext(request,{'teses' : Tese.objects.filter(grupo_idgrupo=1064), 'dados': dados})
	
	return render(request, 'index.html')

def similarityGroups(request):
	dados = []	

	teses = Tese.objects.filter(grupo_idgrupo=1064)
	for t in teses:	
		h = HTMLParser.HTMLParser()

		t.tese = re.sub('<[^>]*>', '', h.unescape(t.tese))

	context = RequestContext(request,{'teses' : teses, 'dados': dados, 'grupo' : Grupo.objects.filter(idgrupo=1064)[0]})

	return render(request, 'similarityGroups.html', context)

def summaryGroups(request):
	dados = []	

	teses = Tese.objects.filter(grupo_idgrupo=1064)
	for t in teses:	
		h = HTMLParser.HTMLParser()

		t.tese = re.sub('<[^>]*>', '', h.unescape(t.tese))

	context = RequestContext(request,{'teses' : teses, 'dados': dados, 'grupo' : Grupo.objects.filter(idgrupo=1064)[0],'summary' : True})

	return render(request, 'similarityGroups.html', context)


def teses(request, tese_id):
	
	teses = Tese.objects.filter(grupo_idgrupo=1064)
	
	i = 0
	while i < len(teses):
		h = HTMLParser.HTMLParser()
		print str(teses[i].idtese) + ' == ' + tese_id
		if str(teses[i].idtese) == tese_id:
			index = re.sub('<[^>]*>', '', h.unescape(teses[i].tese))
			break
		i=i+1


	context = RequestContext(request,{'teses' : teses, 'idteseIndex':index, 'idtese':tese_id, 'grupo' : Grupo.objects.filter(idgrupo=1064)[0]})
	
	return render(request, 'teses.html', context)

def summaryTeses(request, tese_id):

	index = -1
	teses = Tese.objects.filter(grupo_idgrupo=1064)
	
	i = 0
	while i < len(teses):
		h = HTMLParser.HTMLParser()
		print str(teses[i].idtese) + ' == ' + tese_id
		if str(teses[i].idtese) == tese_id:
			index = re.sub('<[^>]*>', '', h.unescape(teses[i].tese))
			break
		i=i+1


	context = RequestContext(request,{'teses' : teses, 'idteseIndex':index, 'idtese':tese_id, 'grupo' : Grupo.objects.filter(idgrupo=1064)[0],'summary' : True})
	
	return render(request, 'teses.html', context)

def clusterizacao(request, debate_id, qtdGrupos=3):
	
## COLOCAR COMO OPÇÃO PARA O USUÁRIO SE ELE QUER AGRUPAR 
## PELO POSICIONAMENTO INICIAL OU FINAL 
	print "view-clusterização em funcionamento!!!"
	inicio = datetime.now()
	print inicio,"view clusterizacao"
	
	yappi.set_clock_type('cpu')
	yappi.start(builtins=True)
	start = time.time()
	
	auxResult = clusterArgInicial(debate_id)
	
	duration = time.time() - start
	stats = yappi.get_func_stats()
	stats.save('clusterArgInicial.out', type = 'callgrind')
	
	
	
	tese = auxResult[5]
	
	
	yappi.set_clock_type('cpu')
	yappi.start(builtins=True)
	start = time.time()
	
#	resultado = gruposArgumentacao(auxResult, qtdeGrupos=3, LSA=True, Normalizacao=True)
# 	resultado = gruposArgumentacao(auxResult, qtdeGrupos=4, LSA=True, Normalizacao=True)
# 	resultado = gruposArgumentacao(auxResult, qtdeGrupos=5, LSA=True, Normalizacao=True)
# 	resultado = gruposArgumentacao(auxResult, qtdeGrupos=6, LSA=True, Normalizacao=True)
	
	resultado = gruposArgumentacao(auxResult, qtdeGrupos=int(qtdGrupos), LSA=None, Normalizacao=True)
	
	duration = time.time() - start
	stats = yappi.get_func_stats()
	stats.save('gruposArgumentacao.out', type = 'callgrind')
	
	grupo1 = resultado[0]
	grupo2 = resultado[1]
	grupo3 = resultado[2]
	grupo4 = resultado[3]
	grupo5 = resultado[4]
	grupo6 = resultado[5]

	
	
	
	context = RequestContext(request,{'results' : [grupo1,grupo2,grupo3,grupo4,\
										len(grupo1),len(grupo2),len(grupo3),len(grupo4), tese, \
										grupo5, len(grupo5), grupo6, len(grupo6)],
										'grupo' : Grupo.objects.filter(idgrupo=1064)[0]})
	
	return render(request, 'clusterizacao.html',context)




def summary(request, debate_id, qtdGrupos=3):
	
	auxResult = clusterFinal(debate_id)
	
	tese = auxResult[5]
	
	resultado = gruposArgumentacao(auxResult, qtdeGrupos=int(qtdGrupos), LSA=None, Normalizacao=True, TAGs=False)
	
	grupo1 = resultado[0]
	grupo2 = resultado[1] 
	grupo3 = resultado[2]
	grupo4 = resultado[3]
	grupo5 = resultado[4]
	grupo6 = resultado[5]

	grupo1str = ""
	grupo1usr = ""
	for g in grupo1:
		aux = g.split("#$#")
		grupo1str += aux[1]
		grupo1usr += aux[0] + "<br/>"

	grupo2str = ""
	grupo2usr = ""
	for g in grupo2:
		aux = g.split("#$#")
		grupo2str += aux[1]
		grupo2usr += aux[0] + "<br/>"

	grupo3str = ""
	grupo3usr = ""
	for g in grupo3:
		aux = g.split("#$#")
		grupo3str += aux[1]
		grupo3usr += aux[0] + "<br/>"

	grupo4str = ""
	grupo4usr = ""
	for g in grupo4:
		aux = g.split("#$#")
		grupo4str += aux[1]
		grupo4usr += aux[0] + "<br/>"

	grupo5str = ""
	grupo5usr = ""
	for g in grupo5:
		aux = g.split("#$#")
		grupo5str += aux[1]
		grupo5usr += aux[0] + "<br/>"

	grupo6str = ""
	grupo6usr = ""
	for g in grupo6:
		aux = g.split("#$#")
		grupo6str += aux[1]
		grupo6usr += aux[0] + "<br/>"

	if int(qtdGrupos) > 2:
		grupo1str = createHtmlData(grupo1str)
	else:
		grupo1str = ""

	if int(qtdGrupos) > 2:
		grupo2str = createHtmlData(grupo2str)
	else:
		grupo2str = ""

	if int(qtdGrupos) > 2:
		grupo3str = createHtmlData(grupo3str)
	else:
		grupo3str = ""

	if int(qtdGrupos) > 3:
		grupo4str = createHtmlData(grupo4str)
	else:
		grupo4str = ""

	if int(qtdGrupos) > 4:
		grupo5str = createHtmlData(grupo5str)
	else:
		grupo5str = ""

	if int(qtdGrupos) > 5:
		grupo6str = createHtmlData(grupo6str)
	else:
		grupo6str = ""



	context = RequestContext(request,{
		'grupo1str' : grupo1str,
		'grupo1usr' : grupo1usr,

		'grupo2str' : grupo2str,
		'grupo2usr' : grupo2usr,

		'grupo3str' : grupo3str,
		'grupo3usr' : grupo3usr,

		'grupo4str' : grupo4str,
		'grupo4usr' : grupo4usr,

		'grupo5str' : grupo5str,
		'grupo5usr' : grupo5usr,

		'grupo6str' : grupo6str,
		'grupo6usr' : grupo6usr,

		})
	
	return render(request, 'summary.html', context)


def createHtmlData(wors):
	tags = make_tags(get_tag_counts(wors)[:30], maxsize=90, colors=COLOR_SCHEMES['audacity'])

	
	data = create_html_data(tags, (600,600), layout=LAYOUT_HORIZONTAL, fontname='PT Sans Regular')

	tags_template = '<li class="cnt" style="top: %(top)dpx; left: %(left)dpx; height: %(height)dpx;"><a class="tag %(cls)s" href="#%(tag)s" style="top: %(top)dpx;\
	    left: %(left)dpx; font-size: %(size)dpx; height: %(height)dpx; line-height:%(lh)dpx;">%(tag)s</a></li>'

	return ''.join([tags_template % link for link in data['links']])