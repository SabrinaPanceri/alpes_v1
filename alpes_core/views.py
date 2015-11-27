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

from alpes_core.models import Tese
from alpes_core import clusterArgFinal
from alpes_core.clusterArgInicial import clusterArgInicial
from alpes_core.clusters import clusters

from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances
from sklearn.feature_extraction.text import CountVectorizer

from alpes_core.ex_kmeans import tfIdf_Kmeans
from alpes_core.ex_lsa import similaridade_lsa
from alpes_core.textProcess import removeA, removePontuacao
import codecs
from pprint import pprint
# 
from alpes_core.lsa_kmeans import LSA_Kmeans
from alpes_core.gruposArgumentacao import gruposArgumentacao
from nltk.cluster import KMeansClusterer, euclidean_distance

# Create your views here.
def home(request):
####################################################################################
## 1) COLOCAR DE FORMA OPCIONAL PARA ESCOLHA DO USUÁRIO
## 2) FAZER TELA QUE APRESENTE TODOS OS DEBATES E QUE O USUÁRIO POSSA ESCOLHER 
####################################################################################	
	dados = []	
	
	context = RequestContext(request,{'teses' : Tese.objects.filter(grupo_idgrupo=1064), 'dados': dados})
	
	
	
	return render(request, 'inicio1.html', context)

def inicial(request):
	
	dados = []	
	
	context = RequestContext(request,{'teses' : Tese.objects.filter(), 'dados': dados})
	
	
	return render(request, 'inicio.html', context)

def indicacao(request, tese_id):
##################################################################################################################
## 1) FAZER TELA COM A OPÇÃO DE INDICAÇÃO DOS REVISORES DE ACORDO COM A ARG INICIAL
## 2) O SELECT DEVE PEGAR TODAS AS ARGUMENTAÇÕES NÃO NULAS DE ACORDO COM O GRUPO E TESE ESCOLHIDAS 
## 3) 
##################################################################################################################	
	if tese_id:
		cursor = connection.cursor()
		cursor.execute("select * from argumento where tese_idtese = " +tese_id+" and posicionamentoinicial is not null")
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
	
	return render(request, 'indicacao.html', context)

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



def posInicial(request, debate_id):
# Cluster usado no artigo SBIE/2015 - Agrupamento pelo Posicionamento Inicial
# Técnica para agrupamento KMeans
#Agrupamento pela argumentação Inicial com K-Means
	
	auxResult = clusterArgInicial(debate_id)

	st_tese = auxResult[0]
	posIni = auxResult[1]
	sw_tese = auxResult[2]
	aux_usu = auxResult[3]
	st_posInicial = auxResult[4]
	tese = auxResult[5]
	
	test_set = st_posInicial
	train_set = st_tese


##########################################################################################
	#Utilizando LSA
	
	base_treinamento = codecs.open('/home/panceri/git/alpes_v1/arquivos/baseTreinamento.txt', 'r', 'UTF8')
	##trocar caminho quando colocar no servidor!!!
	
	treinamento = [removeA(removePontuacao(i)) for i in base_treinamento]
	base_treinamento.close()
# 	print len(treinamento)
	
	# Resultado do calculo de similaridade entre todos os alunos
# 	sim_lsa = similaridade_lsa(treinamento, aux_usu, posIni)
# 	pprint(sim_lsa)


##########################################################################################
#   TESTE COM LSA + KMEANS 
##########################################################################################
# 	pprint(list(enumerate(aux_usu)))
# 	pprint(list(enumerate(posIni)))
	
#TESTE COM BASE DE TREINAMENTO COMPOSTA DE OUTROS TEXTOS 
# 	grupos = LSA_Kmeans(clusters=6, textoTreinamento=treinamento, nomeUsuarios=aux_usu, textoComparacao=posIni)
# 	grupos = LSA_Kmeans(clusters=5, textoTreinamento=treinamento, nomeUsuarios=aux_usu, textoComparacao=posIni)
# 	grupos = LSA_Kmeans(clusters=4, textoTreinamento=treinamento, nomeUsuarios=aux_usu, textoComparacao=posIni)
# 	grupos = LSA_Kmeans(clusters=3, textoTreinamento=treinamento, nomeUsuarios=aux_usu, textoComparacao=posIni)

#TESTE COM BASE DE TREINAMENTO COMPOSTA PELO POSIC. INICIAL	
# 	grupos = LSA_Kmeans(clusters=6, textoTreinamento=posIni, nomeUsuarios=aux_usu, textoComparacao=posIni)
# 	grupos = LSA_Kmeans(clusters=5, textoTreinamento=posIni, nomeUsuarios=aux_usu, textoComparacao=posIni)
# 	grupos = LSA_Kmeans(clusters=4, textoTreinamento=posIni, nomeUsuarios=aux_usu, textoComparacao=posIni)
#	grupos = LSA_Kmeans(clusters=3, textoTreinamento=posIni, nomeUsuarios=aux_usu, textoComparacao=posIni)

	
##########################################################################################	
	#Utilização das funções para calculo do TF-IDF sob a tese e o posInicial
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
# Para n_cluster = 3
# 	grupos = tfIdf_Kmeans(st_posInicial, 3)
	
# Para n_cluster = 4
#	grupos = tfIdf_Kmeans(st_posInicial, 4)
	
# Para n_cluster = 5
#	grupos = tfIdf_Kmeans(st_posInicial, 5)

# Para n_cluster = 6
 	grupos = tfIdf_Kmeans(st_posInicial, 6)
# 	print grupos

	grupo1 = []
	grupo2 = []
	grupo3 = []
	grupo4 = []
	grupo5 = []
	grupo6 = []
	indices = []
	
	for i in range(len(grupos)):
		for j in range(len(grupos[i])):
			if i == 0:
				aux = grupos[i][j]
				texto = "Aluno:"+ aux_usu[aux] + " => Posicionamento Inicial: " +  posIni[aux]
				grupo1.append(texto)
				indices.append(grupos[i][j])				
			elif i == 1:
				aux = grupos[i][j]
				texto = "Aluno:"+ aux_usu[aux] + " => Posicionamento Inicial: " +  posIni[aux]
				grupo2.append(texto)		
				indices.append(grupos[i][j])	
			elif i == 2:
				aux = grupos[i][j]
				texto = "Aluno:"+ aux_usu[aux] + " => Posicionamento Inicial: " +  posIni[aux]
				grupo3.append(texto)
				indices.append(grupos[i][j])
			#para n_clusters = 4
			elif i == 3:
				aux = grupos[i][j]
				texto = "Aluno:"+ aux_usu[aux] + " => Posicionamento Inicial: " +  posIni[aux]
				grupo4.append(texto)
				indices.append(grupos[i][j])
			#para n_clusters = 5
			elif i == 4:
				aux = grupos[i][j]
				texto = "Aluno:"+ aux_usu[aux] + " => Posicionamento Inicial: " +  posIni[aux]
				grupo5.append(texto)
				indices.append(grupos[i][j])
			#para n_clusters = 6
			elif i == 5:
				aux = grupos[i][j]
				texto = "Aluno:"+ aux_usu[aux] + " => Posicionamento Inicial: " +  posIni[aux]
				grupo6.append(texto)
				indices.append(grupos[i][j])
	
	#PARA 3 CLUSTERS
# 	ind_aux = indices[:len(grupo1)]
# 	ind_aux2 = indices[len(ind_aux):len(ind_aux)+len(grupo2)]
# 	ind_aux3 = indices[len(ind_aux)+len(grupo2):]
	
	
	#PARA 4 CLUSTERS		
#	ind_aux = indices[:len(grupo1)]
#	ind_aux2 = indices[len(grupo1):len(grupo1)+len(grupo2)]
#	ind_aux3 = indices[len(grupo1)+len(grupo2):(len(grupo1)+len(grupo2))+len(grupo3)]
#	ind_aux4 = indices[(len(grupo1)+len(grupo2))+len(grupo3):]
#	print "GRUPOS", grupos
#	print "INDICES", indices

#PARA 5 CLUSTERS		
# 	ind_aux = indices[:len(grupo1)]
# # 	print "ind_aux", ind_aux
# # 	print "len_g1", len(grupo1)
# 	ind_aux2 = indices[len(grupo1):len(grupo1)+len(grupo2)]
# # 	print "ind_aux", ind_aux2
# # 	print "len_g2", len(grupo2)
# 	ind_aux3 = indices[len(grupo1)+len(grupo2):(len(grupo1)+len(grupo2))+len(grupo3)]
# # 	print "ind_aux", ind_aux3
# # 	print "len_g3", len(grupo3)
# 	ind_aux4 = indices[(len(grupo1)+len(grupo2)+len(grupo3)):(len(grupo1)+len(grupo2)+len(grupo3))+len(grupo4)]
# # 	print "ind_aux", ind_aux4
# # 	print "len_g4", len(grupo4)
# 	ind_aux5 = indices[(len(grupo1)+len(grupo2)+len(grupo3))+len(grupo4):]
# 	print "ind_aux", ind_aux5
# 	print "len_g5", len(grupo5)


#PARA 6 CLUSTERS		
	ind_aux = indices[:len(grupo1)]
# 	print "ind_aux", ind_aux
# 	print "len_g1", len(grupo1)
	ind_aux2 = indices[len(grupo1):len(grupo1)+len(grupo2)]
# 	print "ind_aux", ind_aux2
# 	print "len_g2", len(grupo2)
	ind_aux3 = indices[len(grupo1)+len(grupo2):(len(grupo1)+len(grupo2))+len(grupo3)]
# 	print "ind_aux", ind_aux3
# 	print "len_g3", len(grupo3)
	ind_aux4 = indices[(len(grupo1)+len(grupo2)+len(grupo3)):(len(grupo1)+len(grupo2)+len(grupo3))+len(grupo4)]
# 	print "ind_aux", ind_aux4
# 	print "len_g4", len(grupo4)
	ind_aux5 = indices[(len(grupo1)+len(grupo2)+len(grupo3))+len(grupo4):(len(grupo1)+len(grupo2)+len(grupo3)+len(grupo4))+len(grupo5)]
# 	print "ind_aux", ind_aux5
# 	print "len_g5", len(grupo5)
	ind_aux6 = indices[(len(grupo1)+len(grupo2)+len(grupo3)+len(grupo4))+len(grupo5):]
# 	print "ind_aux", ind_aux6
# 	print "len_g6", len(grupo6)
	





##########################################################################################
	print "grupo 1", len(grupo1)
	cos = []
	lsaPosIni = []
	lsaUsu =[]

	for y in range(len(ind_aux)):
# 		print "posIni[y]", aux_usu[ind_aux[y]],posIni[ind_aux[y]]
		lsaPosIni.append(posIni[ind_aux[y]])
		lsaUsu.append(aux_usu[ind_aux[y]])
		for x in range(y+1, len(ind_aux)):
			num1 = ind_aux[y]
			num2 = ind_aux[x]
			cos.append(cosine_similarity(tf_idf_matrix[num1], tf_idf_matrix[num2]))
			euc = euclidean_distances(tf_idf_matrix[num1], tf_idf_matrix[num2],squared=True)
# 			print "cosine", cosine_similarity(tf_idf_matrix[num1], tf_idf_matrix[num2])
# 			print "euc", euc

	simLSA = similaridade_lsa(treinamento, lsaUsu, lsaPosIni)
# 	print "simLSA"
# 	pprint(sorted(simLSA, reverse=True))

	simLSA1 = similaridade_lsa(posIni, lsaUsu, lsaPosIni)
# 	print "simLSA1"
# 	pprint(sorted(simLSA1, reverse=True))
# 	print "cos",cos
# 	print "len_cos",len(cos)
	sum_cos = 0

# 	if len(cos) != 0:
# 		for i in cos:
# 			sum_cos = i + sum_cos
# 
# 		print "media = ", sum_cos / len(cos)
# 	else:
# 		print "sem média"

##########################################################################################
# 	print "grupo 2", len(grupo2)
	cos2 = []
	lsaPosIni = []
	lsaUsu =[]
	print lsaPosIni
	print lsaUsu

	for y in range(len(ind_aux2)):
		lsaPosIni.append(posIni[ind_aux2[y]])
		lsaUsu.append(aux_usu[ind_aux2[y]])
		for x in range(y+1, len(ind_aux2)):
			num1 = ind_aux2[y]
			num2 = ind_aux2[x]
			cos2.append(cosine_similarity(tf_idf_matrix[num1], tf_idf_matrix[num2]))
			euc = euclidean_distances(tf_idf_matrix[num1], tf_idf_matrix[num2],squared=True)
# 			print aux_usu[num1],aux_usu[num2]
# 			print "cosine", cosine_similarity(tf_idf_matrix[num1], tf_idf_matrix[num2])
# 			print "euc", euc
# 	print "cos",cos2
# 	print "len_cos",len(cos2)
	simLSA = similaridade_lsa(treinamento, lsaUsu, lsaPosIni)
# 	print "simLSA"
# 	pprint(sorted(simLSA, reverse=True))

	simLSA1 = similaridade_lsa(posIni, lsaUsu, lsaPosIni)
# 	print "simLSA1"
# 	pprint(sorted(simLSA1, reverse=True))


# 	sum_cos = 0
# 	if len(cos2) != 0:
# 		for i in cos2:
# 			sum_cos = i + sum_cos
# 		print "media = ", sum_cos / len(cos2)
# 	else:
# 		print "sem média"

##########################################################################################	
# 	print "grupo 3", len(grupo3)
	cos3 = []	
	lsaPosIni = []
	lsaUsu =[]
# 	print lsaPosIni
# 	print lsaUsu

	for y in range(len(ind_aux3)):
		lsaPosIni.append(posIni[ind_aux3[y]])
		lsaUsu.append(aux_usu[ind_aux3[y]])
		for x in range(y+1, len(ind_aux3)):
			num1 = ind_aux3[y]
			num2 = ind_aux3[x]
			cos3.append(cosine_similarity(tf_idf_matrix[num1], tf_idf_matrix[num2]))
			euc = euclidean_distances(tf_idf_matrix[num1], tf_idf_matrix[num2],squared=True)
# 			print aux_usu[num1],aux_usu[num2]
# 			print "cosine", cosine_similarity(tf_idf_matrix[num1], tf_idf_matrix[num2])
# 			print "euc", euc

# 	print "cos",cos3
# 	print "len_cos",len(cos3)

	simLSA = similaridade_lsa(treinamento, lsaUsu, lsaPosIni)
# 	print "simLSA"
# 	pprint(sorted(simLSA, reverse=True))

	simLSA1 = similaridade_lsa(posIni, lsaUsu, lsaPosIni)
# 	print "simLSA1"
# 	pprint(sorted(simLSA1, reverse=True))

# 	sum_cos = 0
# 	if len(cos3) != 0:
# 		for i in cos3:
# 			sum_cos = i + sum_cos
# 		print "media = ", sum_cos / len(cos3)
# 	else:
# 		print "sem média"

##########################################################################################
# 	print "grupo 4", len(grupo4)
	cos4 = []
	lsaPosIni = []
	lsaUsu =[]
	print lsaPosIni
	print lsaUsu
	for y in range(len(ind_aux4)):
		lsaPosIni.append(posIni[ind_aux4[y]])
		lsaUsu.append(aux_usu[ind_aux4[y]])
		for x in range(y+1, len(ind_aux4)):
			num1 = ind_aux4[y]
			num2 = ind_aux4[x]
			cos4.append(cosine_similarity(tf_idf_matrix[num1], tf_idf_matrix[num2]))
			euc = euclidean_distances(tf_idf_matrix[num1], tf_idf_matrix[num2],squared=True)
# 			print aux_usu[num1],aux_usu[num2]
# 			print "cosine", cosine_similarity(tf_idf_matrix[num1], tf_idf_matrix[num2])
# 			print "euc", euc
 
# 	print "cos",cos4
# 	print "len_cos",len(cos4)
	simLSA = similaridade_lsa(treinamento, lsaUsu, lsaPosIni)
# 	print "simLSA"
# 	pprint(sorted(simLSA, reverse=True))
 
	simLSA1 = similaridade_lsa(posIni, lsaUsu, lsaPosIni)
# 	print "simLSA1"
# 	pprint(sorted(simLSA1, reverse=True))
 
# 	sum_cos = 0
# 	if len(cos4) != 0:
# 		for i in cos4:
# 			sum_cos = i + sum_cos
# 		print "media = ", sum_cos / len(cos4)
# 	else:
# 		print "sem média"


##########################################################################################	
# 	print "grupo 5", len(grupo5)
	cos5 = []
	lsaPosIni = []
	lsaUsu =[]
# 	print lsaPosIni
# 	print lsaUsu
 
	for y in range(len(ind_aux5)):
		lsaPosIni.append(posIni[ind_aux5[y]])
		lsaUsu.append(aux_usu[ind_aux5[y]])
		for x in range(y+1, len(ind_aux5)):
			num1 = ind_aux5[y]
			num2 = ind_aux5[x]
			cos5.append(cosine_similarity(tf_idf_matrix[num1], tf_idf_matrix[num2]))
			euc = euclidean_distances(tf_idf_matrix[num1], tf_idf_matrix[num2],squared=True)
# 			print aux_usu[num1],aux_usu[num2]
# 			print "cosine", cosine_similarity(tf_idf_matrix[num1], tf_idf_matrix[num2])
# 			print "euc", euc
 
# 	print "cos",cos5
# 	print "len_cos", len(cos5)
	simLSA = similaridade_lsa(treinamento, lsaUsu, lsaPosIni)
# 	print "simLSA"
# 	pprint(sorted(simLSA, reverse=True))
 
	simLSA1 = similaridade_lsa(posIni, lsaUsu, lsaPosIni)
# 	print "simLSA1"
# 	pprint(sorted(simLSA1, reverse=True))
 
# 	sum_cos = 0
# 	if len(cos5) != 0:
# 		for i in cos5:
# 			sum_cos = i + sum_cos
# 		print "media = ", sum_cos / len(cos5)
# 	else:
# 		print "sem média"

##########################################################################################
# 	print "grupo 6", len(grupo6)
	cos6 = []
	cos5 = []
	lsaPosIni = []
	lsaUsu =[]
 
	for y in range(len(ind_aux6)):
		lsaPosIni.append(posIni[ind_aux6[y]])
		lsaUsu.append(aux_usu[ind_aux6[y]])
		for x in range(y+1, len(ind_aux6)):
			num1 = ind_aux6[y]
			num2 = ind_aux6[x]
			cos6.append(cosine_similarity(tf_idf_matrix[num1], tf_idf_matrix[num2]))
			euc = euclidean_distances(tf_idf_matrix[num1], tf_idf_matrix[num2],squared=True)
# 			print aux_usu[num1],aux_usu[num2]
# 			print "cosine", cosine_similarity(tf_idf_matrix[num1], tf_idf_matrix[num2])
# 			print "euc", euc
 
# 	print "cos",cos6
# 	print "len_cos",len(cos6)
	simLSA = similaridade_lsa(treinamento, lsaUsu, lsaPosIni)
# 	print "simLSA"
# 	pprint(sorted(simLSA, reverse=True))
 
	simLSA1 = similaridade_lsa(posIni, lsaUsu, lsaPosIni)
# 	print "simLSA1"
# 	pprint(sorted(simLSA1, reverse=True))
 
# 	sum_cos = 0
# 	if len(cos6) != 0:
# 		for i in cos6:
# 			sum_cos = i + sum_cos
# 		print "media = ", sum_cos / len(cos6)
# 	else:
# 		print "sem média"


##########################################################################################

	context = RequestContext(request,{'results' : [grupo1,grupo2,grupo3,grupo4,\
										len(grupo1),len(grupo2),len(grupo3),len(grupo4), tese, \
										grupo5, len(grupo5), grupo6, len(grupo6)]})
	
	
	return render(request, 'posInicial.html',context)


def clusterizacao(request, debate_id):
# TESTE COM CLUSTERIZAÇÃO A PARTIR DO DICIONÁRIO DE SINONIMOS
# utilizar os número de referência dos sinonimos como base para a análise de similaridade
	print "view-clusterização em funcionamento!!!"
	inicio = datetime.now()
	print inicio,"view clusterizacao"
	
	auxResult = clusterArgInicial(debate_id)
	
	tese = auxResult[5]

	resultado = gruposArgumentacao(auxResult, 3, True)
# 	resultado = gruposArgumentacao(auxResult, 4, True/None/False)
# 	resultado = gruposArgumentacao(auxResult, 5, True/None/False)
# 	resultado = gruposArgumentacao(auxResult, 6, True/None/False)
	
	fim = datetime.now()
	print fim
	
	grupo1 = resultado[0]
	grupo2 = resultado[1]
	grupo3 = resultado[2]
	grupo4 = resultado[3]
	grupo5 = resultado[4]
	grupo6 = resultado[5]

	
	
	
	context = RequestContext(request,{'results' : [grupo1,grupo2,grupo3,grupo4,\
										len(grupo1),len(grupo2),len(grupo3),len(grupo4), tese, \
										grupo5, len(grupo5), grupo6, len(grupo6)]})
	
	return render(request, 'posInicial.html',context)


def agrupamentos(request, debate_id):
#Clusterização

	auxResult = clusterArgInicial(debate_id)

	resultado = clusters(auxResult, numCluster=3, lsa_km=False, tfIdf_km=True, treino_externo=False)	

	grupo1 = resultado[0]
	grupo2 = resultado[1]
	grupo3 = resultado[2]
	grupo4 = resultado[3]
	grupo5 = resultado[4]
	grupo6 = resultado[5]
	tese = resultado[6]

	
	context = RequestContext(request,{'results' : [grupo1,grupo2,grupo3,grupo4,\
										len(grupo1),len(grupo2),len(grupo3),len(grupo4), tese, \
										grupo5, len(grupo5), grupo6, len(grupo6)]})
	
	
	return render(request, 'posInicial.html',context)


# def index(request):
#     return render(request,'index.html', {})
# 
# def charts(request):
#     return render(request,'charts.html', {})
# 
# def pages(request):
#     return render(request,'{{request}}.html', {