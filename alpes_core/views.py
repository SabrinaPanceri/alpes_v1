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
from alpes_core.gruposArgumentacao import gruposArgumentacao
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


def teses(request, tese_id):
	if tese_id:
		cursor = connection.cursor()
		#cursor.execute("select `arg`.`posicionamentoinicial` AS `posicionamentoinicial`, `arg`.`argumento` AS `argumento`, `rev`.`revisao` AS `revisao`, `rep`.`replica` AS `replica`, `pos`.`posicionamentofinal` AS `posicionamentofinal` from (((`argumento` `arg` join `revisao` `rev`) join `replica` `rep`) join `posicionamento` `pos`) where ((`arg`.`tese_idtese` = " + idtese + " ) and (`rev`.`argumento_idargumento` = `arg`.`idargumento`) and (`rep`.`revisao_idrevisao` = `rev`.`idrevisao`) and (`arg`.`argumentador_idargumentador` = `pos`.`argumentador_idargumentador`) and (`arg`.`tese_idtese` = `pos`.`tese_idtese`) and (`arg`.`posicionamentoinicial` is not null) and (`arg`.`argumento` is not null) and (`rev`.`revisao` is not null) and (`rep`.`replica` is not null) and (`pos`.`posicionamentofinal` is not null))")
		cursor.execute("select `usr`.`primeironome` as `name`, `posicionamentoinicial` AS `posicionamentoinicial`, `arg`.`argumento` AS `argumento`, `rev`.`revisao` AS `revisao`, `rep`.`replica` AS `replica`, `pos`.`posicionamentofinal` AS `posicionamentofinal` from ((((`argumento` `arg` join `revisao` `rev`) join `replica` `rep`) join `posicionamento` `pos`) join `argumentador` `urg`)join `usuario` `usr`  where ((`arg`.`tese_idtese` = " + tese_id + "  ) and (`rev`.`argumento_idargumento` = `arg`.`idargumento`) and (`rep`.`revisao_idrevisao` = `rev`.`idrevisao`) and (`arg`.`argumentador_idargumentador` = `pos`.`argumentador_idargumentador`) and (`arg`.`tese_idtese` = `pos`.`tese_idtese`) and (`arg`.`posicionamentoinicial` is not null) and (`arg`.`argumentador_idargumentador` = `urg`.`idargumentador`) and(`urg`.`usuario_idusuario` = `usr`.`idusuario`) and(`arg`.`argumento` is not null) and (`rev`.`revisao` is not null) and (`rep`.`replica` is not null) and (`pos`.`posicionamentofinal` is not null))")
		dadosSql = cursor.fetchall()	
	
		h = HTMLParser.HTMLParser()
		allDados = []

		for d in dadosSql:
			allDados.append([re.sub('<[^>]*>', '', h.unescape(d[0])),re.sub('<[^>]*>', '', h.unescape(d[1])),re.sub('<[^>]*>', '', h.unescape(d[2])),re.sub('<[^>]*>', '', h.unescape(d[3])),re.sub('<[^>]*>', '', h.unescape(d[4])),re.sub('<[^>]*>', '', h.unescape(d[5]))])


		dados = []
		for al in allDados:
			valid  = True
			for dd in dados:

				if al[0] == dd[0] and al[1] == dd[1] and al[2] == dd[2]:
					valid = False
					break
				

			if valid:
				dados.append(al)


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


	context = RequestContext(request,{'teses' : teses, 'dados': dados, 'idteseIndex':index, 'idtese':tese_id, 'grupo' : Grupo.objects.filter(idgrupo=1064)[0]})
	
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
	pass
