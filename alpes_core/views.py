#coding: utf-8

from django.shortcuts import render

from alpes_core.models import Tese
from django.template import RequestContext, loader
from django.db import connections, connection

import HTMLParser
import re
# Create your views here.
def home(request):
	cursor = connection.cursor()
	
	dados = []		
	context = RequestContext(request,{'teses' : Tese.objects.filter(grupo_idgrupo=1064), 'dados': dados})
	
	return render(request, 'inicio1.html', context)

def teses(request, tese_id):
	if tese_id:
		cursor = connection.cursor()
		#cursor.execute("select `arg`.`posicionamentoinicial` AS `posicionamentoinicial`, `arg`.`argumento` AS `argumento`, `rev`.`revisao` AS `revisao`, `rep`.`replica` AS `replica`, `pos`.`posicionamentofinal` AS `posicionamentofinal` from (((`argumento` `arg` join `revisao` `rev`) join `replica` `rep`) join `posicionamento` `pos`) where ((`arg`.`tese_idtese` = " + idtese + " ) and (`rev`.`argumento_idargumento` = `arg`.`idargumento`) and (`rep`.`revisao_idrevisao` = `rev`.`idrevisao`) and (`arg`.`argumentador_idargumentador` = `pos`.`argumentador_idargumentador`) and (`arg`.`tese_idtese` = `pos`.`tese_idtese`) and (`arg`.`posicionamentoinicial` is not null) and (`arg`.`argumento` is not null) and (`rev`.`revisao` is not null) and (`rep`.`replica` is not null) and (`pos`.`posicionamentofinal` is not null))")
		cursor.execute("select `usr`.`primeironome` as `name`, `posicionamentoinicial` AS `posicionamentoinicial`, `arg`.`argumento` AS `argumento`, `rev`.`revisao` AS `revisao`, `rep`.`replica` AS `replica`, `pos`.`posicionamentofinal` AS `posicionamentofinal` from ((((`argumento` `arg` join `revisao` `rev`) join `replica` `rep`) join `posicionamento` `pos`) join `argumentador` `urg`)join `usuario` `usr`  where ((`arg`.`tese_idtese` = " + tese_id + "  ) and (`rev`.`argumento_idargumento` = `arg`.`idargumento`) and (`rep`.`revisao_idrevisao` = `rev`.`idrevisao`) and (`arg`.`argumentador_idargumentador` = `pos`.`argumentador_idargumentador`) and (`arg`.`tese_idtese` = `pos`.`tese_idtese`) and (`arg`.`posicionamentoinicial` is not null) and (`arg`.`argumentador_idargumentador` = `urg`.`idargumentador`) and(`urg`.`usuario_idusuario` = `usr`.`idusuario`) and(`arg`.`argumento` is not null) and (`rev`.`revisao` is not null) and (`rep`.`replica` is not null) and (`pos`.`posicionamentofinal` is not null))")
		dadosSql = cursor.fetchall()	
	
		h = HTMLParser.HTMLParser()
		dados = []

		for d in dadosSql:
		
			dados.append([re.sub('<[^>]*>', '', h.unescape(d[0])),re.sub('<[^>]*>', '', h.unescape(d[1])),re.sub('<[^>]*>', '', h.unescape(d[2])),re.sub('<[^>]*>', '', h.unescape(d[3])),re.sub('<[^>]*>', '', h.unescape(d[4])),re.sub('<[^>]*>', '', h.unescape(d[5]))])
	else:
		dados = []


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


	context = RequestContext(request,{'teses' : teses, 'dados': dados, 'idteseIndex':index})
	
	return render(request, 'inicio1.html', context)


def debate(request, debate_id):
	return render(request, 'debate.html')
# def index(request):
#     return render(request,'index.html', {})
# 
# def charts(request):
#     return render(request,'charts.html', {})
# 
# def pages(request):
#     return render(request,'{{request}}.html', {})