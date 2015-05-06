#coding: utf-8

from django.shortcuts import render

from alpes_core.models import Tese
from django.template import RequestContext
from django.db import connection
from alpes_core.clusterArgFinal import clusterArgFinal
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import HTMLParser
import re

# Create your views here.
def home(request):
	
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


	context = RequestContext(request,{'teses' : teses, 'dados': dados, 'idteseIndex':index, 'idtese':tese_id})
	
	return render(request, 'inicio1.html', context)


def debate(request, debate_id):
	
	auxResult = clusterArgFinal(debate_id)

	st_tese = auxResult[0]
	posFinal = auxResult[1]
	sw_tese = auxResult[2]
	aux_usu = auxResult[3]
	st_posFinal = auxResult[4]

	test_set = st_posFinal
	train_set = st_tese

	grupo1 = []
	grupo2 = []
	grupo3 = []
	grupo4 = []
	nao_sim = []
	test = []

	#Utilização das funções para calculo do TF-IDF sob a tese e o posFinal
	vectorizer = CountVectorizer()
	vectorizer.fit_transform(train_set)
	count_vectorizer = CountVectorizer()
	count_vectorizer.fit_transform(train_set) 
	count_vectorizer.vocabulary_
	freq_term_matrix = count_vectorizer.transform(test_set)
	tfidf = TfidfTransformer(norm="l2")
	tfidf.fit(freq_term_matrix)
	tf_idf_matrix = tfidf.transform(freq_term_matrix)

	#Tratamento das matrizes geradas pelo algoritmo de TF-IDF com a aplicação do cálculo do 
	#coseno entre os vetores - Cosine Similaridade
	for i in range(0, len(test_set)):
		for j in range(i+1, len(test_set)):
			#Calculo da similaridade de cossenos 
			cos = cosine_similarity(tf_idf_matrix[i], tf_idf_matrix[j])
			if cos >= 0.7 and cos <= 1 and \
	            (aux_usu[i]+" com "+aux_usu[j]) not in grupo1 and \
	            (aux_usu[i]+" com "+aux_usu[j]) not in grupo2 and \
	            (aux_usu[i]+" com "+aux_usu[j]) not in grupo3:
				grupo1.append(aux_usu[i]+": " + posFinal[i] + "\n COM \n"+aux_usu[j]+": "+ posFinal[j] + " Sim = " +str(cos) + "\n")
				
			elif cos >= 0.4 and cos < 0.7 and \
	            (aux_usu[i]+" com "+aux_usu[j]) not in grupo1 and \
	            (aux_usu[i]+" com "+aux_usu[j]) not in grupo2 and \
	            (aux_usu[i]+" com "+aux_usu[j]) not in grupo3:
				grupo2.append(aux_usu[i]+":" + posFinal[i] + "\n COM \n"+aux_usu[j]+": "+ posFinal[j] + " Sim = " +str(cos) + "\n")
			elif cos >= 0.2 and cos < 0.4 and \
	            (aux_usu[i]+" com "+aux_usu[j]) not in grupo1 and \
	            (aux_usu[i]+" com "+aux_usu[j]) not in grupo2 and \
	            (aux_usu[i]+" com "+aux_usu[j]) not in grupo3 :
				grupo3.append(aux_usu[i]+": " + posFinal[i] + "\n COM \n"+aux_usu[j]+": "+ posFinal[j] + " Sim = " +str(cos) + "\n")
			elif cos >= 0.1 and cos < 0.2 and \
	            (aux_usu[i]+" com "+aux_usu[j]) not in grupo1 and \
	            (aux_usu[i]+" com "+aux_usu[j]) not in grupo2 and \
	            (aux_usu[i]+" com "+aux_usu[j]) not in grupo3 :
				grupo4.append(aux_usu[i]+": " + posFinal[i] + "\n COM \n"+aux_usu[j]+": "+ posFinal[j] + " Sim = " +str(cos) + "\n")
			else:
				nao_sim.append(aux_usu[i]+": " + posFinal[i] + "\n COM \n"+aux_usu[j]+": "+ posFinal[j] + " Sim = " +str(cos) + "\n")

	context = RequestContext(request,{'results' : [grupo1,grupo2,grupo3,grupo4,nao_sim, test]})
	return render(request, 'debate.html',context)


# def index(request):
#     return render(request,'index.html', {})
# 
# def charts(request):
#     return render(request,'charts.html', {})
# 
# def pages(request):
#     return render(request,'{{request}}.html', {})