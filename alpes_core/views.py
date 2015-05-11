#coding: utf-8

from django.shortcuts import render

from alpes_core.models import Tese
from django.template import RequestContext
from django.db import connection
from alpes_core.clusterArgFinal import clusterArgFinal
from alpes_core.clusterArgInicial import clusterArgInicial
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances
from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.cluster.k_means_ import KMeans
# from nltk.cluster import KMeansClusterer
# from alpes_core import ex_kmeans

import HTMLParser
import re
from alpes_core.ex_kmeans import cluster_texts


# from nltk.cluster import KMeansClusterer, euclidean_distance

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

def debate(request, debate_id): #Cluster pela argumentação FINAL
	
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
			
			if cos >= 0.9 and cos <= 1 and \
	            (aux_usu[i]+" com "+aux_usu[j]) not in grupo1 and \
	            (aux_usu[i]+" com "+aux_usu[j]) not in grupo2 and \
	            (aux_usu[i]+" com "+aux_usu[j]) not in grupo3:
				grupo1.append(aux_usu[i]+": " + posFinal[i] + "\n COM \n"+aux_usu[j]+": "+ posFinal[j] + " Sim = " +str(cos) + "\n")
			elif cos >= 0.7 and cos < 0.8 and \
	            (aux_usu[i]+" com "+aux_usu[j]) not in grupo1 and \
	            (aux_usu[i]+" com "+aux_usu[j]) not in grupo2 and \
	            (aux_usu[i]+" com "+aux_usu[j]) not in grupo3:
				grupo2.append(aux_usu[i]+":" + posFinal[i] + "\n COM \n"+aux_usu[j]+": "+ posFinal[j] + " Sim = " +str(cos) + "\n")
			elif cos >= 0.6 and cos < 0.7 and \
	            (aux_usu[i]+" com "+aux_usu[j]) not in grupo1 and \
	            (aux_usu[i]+" com "+aux_usu[j]) not in grupo2 and \
	            (aux_usu[i]+" com "+aux_usu[j]) not in grupo3 :
				grupo3.append(aux_usu[i]+": " + posFinal[i] + "\n COM \n"+aux_usu[j]+": "+ posFinal[j] + " Sim = " +str(cos) + "\n")
			elif cos >= 0.5 and cos < 0.6 and \
	            (aux_usu[i]+" com "+aux_usu[j]) not in grupo1 and \
	            (aux_usu[i]+" com "+aux_usu[j]) not in grupo2 and \
	            (aux_usu[i]+" com "+aux_usu[j]) not in grupo3 :
				grupo4.append(aux_usu[i]+": " + posFinal[i] + "\n COM \n"+aux_usu[j]+": "+ posFinal[j] + " Sim = " +str(cos) + "\n")
			else:
			# o corte para considerar não similares é 50% de semelhança entre os textos
				nao_sim.append(aux_usu[i]+": " + posFinal[i] + "\n COM \n"+aux_usu[j]+": "+ posFinal[j] + " Sim = " +str(cos) + "\n")

	context = RequestContext(request,{'results' : [grupo1,grupo2,grupo3,grupo4,nao_sim, test]})
	return render(request, 'debate.html',context)



# Cluster usado no artigo SBIE/2015 - Agrupamento pelo Posicionamento Inicial
# Técnica para agrupamento KMeans

def posInicial(request, debate_id):
	
	auxResult = clusterArgInicial(debate_id)

	st_tese = auxResult[0]
	posInicial = auxResult[1]
	sw_tese = auxResult[2]
	aux_usu = auxResult[3]
	st_posInicial = auxResult[4]
	tese = auxResult[5]
	
	test_set = st_posInicial
	train_set = st_tese
	
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
	
	#Clusterização utilizando Tf-IDF e K-Means
	#Argumento que será clusterizado, e quandidade de clusters
	grupos = cluster_texts(st_posInicial, 3)

	grupo1 = []
	grupo2 = []
	grupo3 = []
	indices = []
	
	for i in range(len(grupos)):
		for j in range(len(grupos[i])):
			if i == 0:
				aux = grupos[i][j]
				texto = "Aluno:"+ aux_usu[aux] + " => Posicionamento Inicial: " +  posInicial[aux]
				grupo1.append(texto)
				indices.append(grupos[i][j])
			elif i == 1:
				aux = grupos[i][j]
				texto = "Aluno:"+ aux_usu[aux] + " => Posicionamento Inicial: " +  posInicial[aux]
				grupo2.append(texto)		
				indices.append(grupos[i][j])	
			elif i == 2:
				aux = grupos[i][j]
				texto = "Aluno:"+ aux_usu[aux] + " => Posicionamento Inicial: " +  posInicial[aux]
				grupo3.append(texto)
				indices.append(grupos[i][j])
			
	ind_aux = indices[:len(grupo1)]
	ind_aux2 = indices[len(ind_aux):len(ind_aux)+len(grupo2)]
	ind_aux3 = indices[len(ind_aux)+len(grupo2):]
	
	print "grupo 1"
	for y in range(len(ind_aux)):
		for x in range(y+1, len(ind_aux)):
			num1 = ind_aux[y]
			num2 = ind_aux[x]
			cos = cosine_similarity(tf_idf_matrix[num1], tf_idf_matrix[num2])
			euc = euclidean_distances(tf_idf_matrix[num1], tf_idf_matrix[num2],squared=True)
			print aux_usu[num1],aux_usu[num2]
			print "cos",cos
			print "euc", euc

	print "grupo 2"
	for y in range(len(ind_aux2)):
		for x in range(y+1, len(ind_aux2)):
			num1 = ind_aux2[y]
			num2 = ind_aux2[x]
			cos = cosine_similarity(tf_idf_matrix[num1], tf_idf_matrix[num2])
			euc = euclidean_distances(tf_idf_matrix[num1], tf_idf_matrix[num2])
			print aux_usu[num1],aux_usu[num2]
			print "cos",cos
			print "euc", euc
			
	print "grupo 3"
	for y in range(len(ind_aux3)):
		for x in range(y+1, len(ind_aux3)):
			num1 = ind_aux3[y]
			num2 = ind_aux3[x]
			cos = cosine_similarity(tf_idf_matrix[num1], tf_idf_matrix[num2])
			euc = euclidean_distances(tf_idf_matrix[num1], tf_idf_matrix[num2])
			print aux_usu[num1],aux_usu[num2]
			print "cos",cos
			print "euc", euc
		
	
	context = RequestContext(request,{'results' : [grupo1,grupo2,grupo3,len(grupo1),len(grupo2),len(grupo3), tese]})
	return render(request, 'posInicial.html',context)


# def index(request):
#     return render(request,'index.html', {})
# 
# def charts(request):
#     return render(request,'charts.html', {})
# 
# def pages(request):
#     return render(request,'{{request}}.html', {})