# -*- coding: utf-8 -*-
##################################################################
### CÓDIGO DESENVOLVIDO POR SABRINA SIQUEIRA PANCERI            ##
### PROTÓTIPO DE SUA  DISSERTAÇÃO DE MESTRADO                   ##
### ESSE CÓDIGO PODE SER COPIADO, ALTERADO E DISTRIBUÍDO        ##
### DESDE QUE SUA FONTE SEJA REFERENCIADA                       ##
### PARA MAIS INFORMAÇÕES, ENTRE EM CONTATO ATRAVÉS DO EMAIL    ##
### SABRINASPANCERI@GMAIL.COM                                   ##
##################################################################

from alpes_core.lsa_kmeans import LSA_Kmeans
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances
from sklearn.feature_extraction.text import CountVectorizer

from alpes_core.ex_kmeans import tfIdf_Kmeans
from alpes_core.ex_lsa import similaridade_lsa
from alpes_core.textProcess import removeA, removePontuacao
import codecs
from pprint import pprint
from datetime import datetime

import yappi
import time

##################################################################################################################
## 1- COLOCAR NA INTERFACE A OPÇÃO DE DIVIDIR EM QUANTOS GRUPOS O PROFESSOR QUER DIVIDIR OS ALUNOS             ###
## 2- COLOCAR A OPÇÃO DE ESCOLHAR APLICAR LSA COM O ENVIO DE MATERIAIS OU A PARTIR DAS PRÓPRIAS ARGUMENTAÇÕES  ###
## 3- FAZER "SWITCH" PARA ESSAS OPÇÕES E COLOCAR NESTA FUNÇÃO                                                  ###
## 4- LINKAR ESSA FUNÇÃO NA VIEW DE TESTE (POSINICIAL1)                                                        ###
## 5- CLUSTERIZAÇÃO FEITA A PARTIR DOS TERMOS NORMALIZADOS!!!!                                                 ###
##                                                                                                             ###
##################################################################################################################
## EXPLICAÇÃO DOS PARÂMETROS:                                                                                   ##
## qtdeGrupos = quantidade de grupos em que os alunos deverão ser divididos                                     ##
## LSA = utiliza LSA=True com base nos argumentos por PADRÃO; SE LSA=False, utiliza o materiais didático enviado##
# pelo professor como base para criação dos dicionários para análise                                            ##
## auxResult = Passa todos os resultados encontrados com a aplicação da função clusterArgInicial + idTese       ##
##                                                                                                              ##
##################################################################################################################

def gruposArgumentacao(auxResult, qtdeGrupos=3, LSA=None, Normalizacao=True):
    inicio = datetime.now()
    print inicio,"gruposArgumentacao"
    yappi.set_clock_type('cpu')
    yappi.start(builtins=True)
    start = time.time()
    

    grupos = []
    tese = auxResult[5]

    posInicial_Normalizado = auxResult[6]
    
    
## dicSin = contém o dicionario com os termos sinonimos já relacionados (relaciona as palavras digitadas pelos alunos com
## o arquivo da wordnet, destaca as relações de sinonimias e apresenta o radical do termo (stemm aplicado) vinculado aos
## numeros das linha aonde estão os seus similares na wordnet    
    
    st_tese = auxResult[0] #texto da tese com aplicação de stemmer
    posIni = auxResult[1] #texto original da argumentação
    sw_tese = auxResult[2] 
    aux_usu = auxResult[3]
    st_posInicial = auxResult[4]
    
    
    base_treinamento = codecs.open('/home/panceri/git/alpes_v1/arquivos/baseTreinamento.txt', 'r', 'UTF8')
        
    treinamento = [removeA(removePontuacao(i)) for i in base_treinamento] 
    # ALTERAR PARA PEGAR DADOS DA INTERFACE (CAIXA DE TEXTO)
    # OU COLOCAR OPÇÃO DE ENVIO DE ARQUIVO .TXT E ABRIR ESSES PARA USAR COMO BASE
    
    base_treinamento.close()

    
##########################################################################################
### ABORDAGEM (1): UTILIZAR O ARGUMENTO COMO BASE PARA CRIAÇÃO DOS DICIONÁRIOS DO LSA  ###
##########################################################################################

#BASE DE TREINAMENTO COMPOSTA PELAS ARGUMENTAÇÕES DOS ALUNOS
    if LSA == True and Normalizacao == False:
        
        print "if LSA == True and Normalizacao == False:"
        
        if qtdeGrupos == 3:
            grupos = LSA_Kmeans(clusters=3, textoTreinamento=posIni, nomeUsuarios=aux_usu, textoComparacao=posIni)
        elif qtdeGrupos == 4:
            grupos = LSA_Kmeans(clusters=4, textoTreinamento=posIni, nomeUsuarios=aux_usu, textoComparacao=posIni)
        elif qtdeGrupos == 5:
            grupos = LSA_Kmeans(clusters=5, textoTreinamento=posIni, nomeUsuarios=aux_usu, textoComparacao=posIni)
        elif qtdeGrupos==6:
            grupos = LSA_Kmeans(clusters=6, textoTreinamento=posIni, nomeUsuarios=aux_usu, textoComparacao=posIni)
        else:
            print "ERRO"

###########################################################################################
### ABORDAGEM (2): UTILIZAR OUTROS TEXTOS COMO BASE PARA CRIAÇÃO DOS DICIONÁRIOS DO LSA ###
###########################################################################################

#BASE DE TREINAMENTO COMPOSTA DE MATERIAIS DIDÁTICOS INDICADOS PELO PROFESSOR         
    elif LSA == False and Normalizacao == False:
        
        print "elif LSA == False and Normalizacao == False:"
        
        if qtdeGrupos == 3:
            grupos = LSA_Kmeans(clusters=3, textoTreinamento=treinamento, nomeUsuarios=aux_usu, textoComparacao=posIni)
        elif qtdeGrupos == 4:
            grupos = LSA_Kmeans(clusters=4, textoTreinamento=treinamento, nomeUsuarios=aux_usu, textoComparacao=posIni)
        elif qtdeGrupos == 5:
            grupos = LSA_Kmeans(clusters=5, textoTreinamento=treinamento, nomeUsuarios=aux_usu, textoComparacao=posIni)
        elif qtdeGrupos == 6:
            grupos = LSA_Kmeans(clusters=6, textoTreinamento=treinamento, nomeUsuarios=aux_usu, textoComparacao=posIni)
        else:
            print "ERRO"
            exit()    
            
#######################################################################################################
### ABORDAGEM (3): UTILIZAR O ARGUMENTO NORMALIZADO COMO BASE PARA CRIAÇÃO DOS DICIONÁRIOS DO LSA  ###
######################################################################################################

#BASE DE TREINAMENTO COMPOSTA DE MATERIAIS DIDÁTICOS INDICADOS PELO PROFESSOR         
    elif LSA == True and Normalizacao == True:
        
        print "elif LSA == True and Normalizacao == True:"
        
        if qtdeGrupos == 3:
            grupos = LSA_Kmeans(clusters=3, textoTreinamento=posInicial_Normalizado, nomeUsuarios=aux_usu, textoComparacao=posInicial_Normalizado)
        elif qtdeGrupos == 4:
            grupos = LSA_Kmeans(clusters=4, textoTreinamento=posInicial_Normalizado, nomeUsuarios=aux_usu, textoComparacao=posInicial_Normalizado)
        elif qtdeGrupos == 5:
            grupos = LSA_Kmeans(clusters=5, textoTreinamento=posInicial_Normalizado, nomeUsuarios=aux_usu, textoComparacao=posInicial_Normalizado)
        elif qtdeGrupos == 6:
            grupos = LSA_Kmeans(clusters=6, textoTreinamento=posInicial_Normalizado, nomeUsuarios=aux_usu, textoComparacao=posInicial_Normalizado)
        else:
            print "ERRO"
            exit()    
            
            

##########################################################################################
### ABORDAGEM (4): UTILIZAÇÃO DO K-MEANS PURO COM TF-IDF                               ###
##########################################################################################
    
    elif LSA == None and Normalizacao == False:
        
        print "elif LSA == None and Normalizacao == False:"
        test_set = st_posInicial
        train_set = st_tese
    
### Utilização das funções para calculo do TF-IDF com a tese e o posInicial
### Funções implementadas com base na SkLearn
        vectorizer = CountVectorizer()
        vectorizer.fit_transform(test_set)
        count_vectorizer = CountVectorizer()
        count_vectorizer.fit_transform(train_set) 
        count_vectorizer.vocabulary_
        freq_term_matrix = count_vectorizer.transform(test_set)
        tfidf = TfidfTransformer(norm="l2")
        tfidf.fit(freq_term_matrix)
        tf_idf_matrix = tfidf.transform(freq_term_matrix)
       
        
        if qtdeGrupos == 3:
            grupos = tfIdf_Kmeans(st_posInicial, 3)
        elif qtdeGrupos == 4:
            grupos = tfIdf_Kmeans(st_posInicial, 4)
        elif qtdeGrupos == 5:
            grupos = tfIdf_Kmeans(st_posInicial, 5)
        elif qtdeGrupos == 6:
            grupos = tfIdf_Kmeans(st_posInicial, 6)
        else:
            print "ERRO"
            exit()

##########################################################################################
### ABORDAGEM (5): UTILIZAÇÃO DO K-MEANS PURO COM TF-IDF                               ###
### COM DADOS NORMALIZADOS                                                             ###
##########################################################################################

### Calculo com base nos textos normalizados!!!    
    
    elif LSA == None and Normalizacao == True:
        
        print "elif LSA == None and Normalizacao == True:"
        
        test_set = posInicial_Normalizado
        train_set = st_tese
    
### Utilização das funções para calculo do TF-IDF com a tese e o posInicial
### Funções implementadas com base na SkLearn
        vectorizer = CountVectorizer()
        vectorizer.fit_transform(test_set)
        count_vectorizer = CountVectorizer()
        count_vectorizer.fit_transform(train_set) 
        count_vectorizer.vocabulary_
        freq_term_matrix = count_vectorizer.transform(test_set)
        tfidf = TfidfTransformer(norm="l2")
        tfidf.fit(freq_term_matrix)
        tf_idf_matrix = tfidf.transform(freq_term_matrix)
       
        
        if qtdeGrupos == 3:
            grupos = tfIdf_Kmeans(posInicial_Normalizado, 3)
        elif qtdeGrupos == 4:
            grupos = tfIdf_Kmeans(posInicial_Normalizado, 4)
        elif qtdeGrupos == 5:
            grupos = tfIdf_Kmeans(posInicial_Normalizado, 5)
        elif qtdeGrupos == 6:
            grupos = tfIdf_Kmeans(posInicial_Normalizado, 6)
        else:
            print "ERRO"
            exit()

##########################################################################################
### RESULTADOS - INDEPENDEM DA ABORDAGEM                                               ###
##########################################################################################
    grupo1 = []
    grupo2 = []
    grupo3 = []
    grupo4 = []
    grupo5 = []
    grupo6 = []
    indices = []
    ind_aux = 0
    ind_aux2 = 0
    ind_aux3 = 0
    ind_aux4 = 0
    ind_aux5 = 0
    ind_aux6 = 0
    
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
    
    if qtdeGrupos == 3:
        ind_aux = indices[:len(grupo1)]
        ind_aux2 = indices[len(ind_aux):len(ind_aux)+len(grupo2)]
        ind_aux3 = indices[len(ind_aux)+len(grupo2):]
        
    elif qtdeGrupos == 4:
        ind_aux = indices[:len(grupo1)]
        ind_aux2 = indices[len(grupo1):len(grupo1)+len(grupo2)]
        ind_aux3 = indices[len(grupo1)+len(grupo2):(len(grupo1)+len(grupo2))+len(grupo3)]
        ind_aux4 = indices[(len(grupo1)+len(grupo2))+len(grupo3):]
        print "GRUPOS", grupos
        print "INDICES", indices
    elif qtdeGrupos == 5:        
        ind_aux = indices[:len(grupo1)]
        print "ind_aux", ind_aux
        print "len_g1", len(grupo1)
        ind_aux2 = indices[len(grupo1):len(grupo1)+len(grupo2)]
        print "ind_aux", ind_aux2
        print "len_g2", len(grupo2)
        ind_aux3 = indices[len(grupo1)+len(grupo2):(len(grupo1)+len(grupo2))+len(grupo3)]
        print "ind_aux", ind_aux3
        print "len_g3", len(grupo3)
        ind_aux4 = indices[(len(grupo1)+len(grupo2)+len(grupo3)):(len(grupo1)+len(grupo2)+len(grupo3))+len(grupo4)]
        print "ind_aux", ind_aux4
        print "len_g4", len(grupo4)
        ind_aux5 = indices[(len(grupo1)+len(grupo2)+len(grupo3))+len(grupo4):]
        print "ind_aux", ind_aux5
        print "len_g5", len(grupo5)
    elif qtdeGrupos == 6:
        ind_aux = indices[:len(grupo1)]
        print "ind_aux", ind_aux
        print "len_g1", len(grupo1)
        ind_aux2 = indices[len(grupo1):len(grupo1)+len(grupo2)]
        print "ind_aux", ind_aux2
        print "len_g2", len(grupo2)
        ind_aux3 = indices[len(grupo1)+len(grupo2):(len(grupo1)+len(grupo2))+len(grupo3)]
        print "ind_aux", ind_aux3
        print "len_g3", len(grupo3)
        ind_aux4 = indices[(len(grupo1)+len(grupo2)+len(grupo3)):(len(grupo1)+len(grupo2)+len(grupo3))+len(grupo4)]
        print "ind_aux", ind_aux4
        print "len_g4", len(grupo4)
        ind_aux5 = indices[(len(grupo1)+len(grupo2)+len(grupo3))+len(grupo4):(len(grupo1)+len(grupo2)+len(grupo3)+len(grupo4))+len(grupo5)]
        print "ind_aux", ind_aux5
        print "len_g5", len(grupo5)
        ind_aux6 = indices[(len(grupo1)+len(grupo2)+len(grupo3)+len(grupo4))+len(grupo5):]
        print "ind_aux", ind_aux6
        print "len_g6", len(grupo6)
    else:
        print "ERRO"
        exit()
    
# ##########################################################################################
# ### IMPRESSÃO DOS GRUPOS NO CONSOLE - PARA CONFERÊNCIA (COMENTAR DEPOIS)               ###
# ##########################################################################################
# 
# ##########################################################################################
# ## UTILIZADO PARA VALIDAR O CÁLCULO REALIZADO E IMPRIMI-LO                              ##
# ##########################################################################################
#     test_set = st_posInicial
#     train_set = st_tese
#     vectorizer = CountVectorizer()
#     vectorizer.fit_transform(train_set)
#     count_vectorizer = CountVectorizer()
#     count_vectorizer.fit_transform(train_set) 
#     count_vectorizer.vocabulary_
#     freq_term_matrix = count_vectorizer.transform(test_set)
#     tfidf = TfidfTransformer(norm="l2")
#     tfidf.fit(freq_term_matrix)
#     tf_idf_matrix = tfidf.transform(freq_term_matrix)
# ##########################################################################################
#     
#      
#     print "grupo 1", len(grupo1)
#     cos = []
#     lsaPosIni = []
#     lsaUsu =[]
#  
#     for y in range(len(ind_aux)):
#         print "posIni[y]", aux_usu[ind_aux[y]],posIni[ind_aux[y]]
#         lsaPosIni.append(posIni[ind_aux[y]])
#         lsaUsu.append(aux_usu[ind_aux[y]])
#         for x in range(y+1, len(ind_aux)):
#             num1 = ind_aux[y]
#             num2 = ind_aux[x]
#             cos.append(cosine_similarity(tf_idf_matrix[num1], tf_idf_matrix[num2]))
#             euc = euclidean_distances(tf_idf_matrix[num1], tf_idf_matrix[num2],squared=True)
#             print "cosine", cosine_similarity(tf_idf_matrix[num1], tf_idf_matrix[num2])
#             print "euc", euc
#  
#     simLSA = similaridade_lsa(treinamento, lsaUsu, lsaPosIni)
#     print "simLSA"
#     pprint(sorted(simLSA, reverse=True))
#  
#     simLSA1 = similaridade_lsa(posIni, lsaUsu, lsaPosIni)
#     print "simLSA1"
#     pprint(sorted(simLSA1, reverse=True))
#     print "cos",cos
#     print "len_cos",len(cos)
#     sum_cos = 0
#  
#     if len(cos) != 0:
#         for i in cos:
#             sum_cos = i + sum_cos
#   
#         print "media = ", sum_cos / len(cos)
#     else:
#         print "sem média"
#  
# ##########################################################################################
#     print "grupo 2", len(grupo2)
#     cos2 = []
#     lsaPosIni = []
#     lsaUsu =[]
#     print lsaPosIni
#     print lsaUsu
#  
#     for y in range(len(ind_aux2)):
#         lsaPosIni.append(posIni[ind_aux2[y]])
#         lsaUsu.append(aux_usu[ind_aux2[y]])
#         for x in range(y+1, len(ind_aux2)):
#             num1 = ind_aux2[y]
#             num2 = ind_aux2[x]
#             cos2.append(cosine_similarity(tf_idf_matrix[num1], tf_idf_matrix[num2]))
#             euc = euclidean_distances(tf_idf_matrix[num1], tf_idf_matrix[num2],squared=True)
#             print aux_usu[num1],aux_usu[num2]
#             print "cosine", cosine_similarity(tf_idf_matrix[num1], tf_idf_matrix[num2])
#             print "euc", euc
#     print "cos",cos2
#     print "len_cos",len(cos2)
#     simLSA = similaridade_lsa(treinamento, lsaUsu, lsaPosIni)
#     print "simLSA"
#     pprint(sorted(simLSA, reverse=True))
#  
#     simLSA1 = similaridade_lsa(posIni, lsaUsu, lsaPosIni)
#     print "simLSA1"
#     pprint(sorted(simLSA1, reverse=True))
#  
#  
#     sum_cos = 0
#     if len(cos2) != 0:
#         for i in cos2:
#             sum_cos = i + sum_cos
#         print "media = ", sum_cos / len(cos2)
#     else:
#         print "sem média"
#  
# ##########################################################################################    
#     print "grupo 3", len(grupo3)
#     cos3 = []    
#     lsaPosIni = []
#     lsaUsu =[]
#     print lsaPosIni
#     print lsaUsu
#  
#     for y in range(len(ind_aux3)):
#         lsaPosIni.append(posIni[ind_aux3[y]])
#         lsaUsu.append(aux_usu[ind_aux3[y]])
#         for x in range(y+1, len(ind_aux3)):
#             num1 = ind_aux3[y]
#             num2 = ind_aux3[x]
#             cos3.append(cosine_similarity(tf_idf_matrix[num1], tf_idf_matrix[num2]))
#             euc = euclidean_distances(tf_idf_matrix[num1], tf_idf_matrix[num2],squared=True)
#             print aux_usu[num1],aux_usu[num2]
#             print "cosine", cosine_similarity(tf_idf_matrix[num1], tf_idf_matrix[num2])
#             print "euc", euc
#  
#     print "cos",cos3
#     print "len_cos",len(cos3)
#  
#     simLSA = similaridade_lsa(treinamento, lsaUsu, lsaPosIni)
#     print "simLSA"
#     pprint(sorted(simLSA, reverse=True))
#  
#     simLSA1 = similaridade_lsa(posIni, lsaUsu, lsaPosIni)
#     print "simLSA1"
#     pprint(sorted(simLSA1, reverse=True))
#  
#     sum_cos = 0
#     if len(cos3) != 0:
#         for i in cos3:
#             sum_cos = i + sum_cos
#         print "media = ", sum_cos / len(cos3)
#     else:
#         print "sem média"
 
#########################################################################################
#     print "grupo 4", len(grupo4)
#     cos4 = []
#     lsaPosIni = []
#     lsaUsu =[]
#     print lsaPosIni
#     print lsaUsu
#     for y in range(len(ind_aux4)):
#         lsaPosIni.append(posIni[ind_aux4[y]])
#         lsaUsu.append(aux_usu[ind_aux4[y]])
#         for x in range(y+1, len(ind_aux4)):
#             num1 = ind_aux4[y]
#             num2 = ind_aux4[x]
#             cos4.append(cosine_similarity(tf_idf_matrix[num1], tf_idf_matrix[num2]))
#             euc = euclidean_distances(tf_idf_matrix[num1], tf_idf_matrix[num2],squared=True)
#             print aux_usu[num1],aux_usu[num2]
#             print "cosine", cosine_similarity(tf_idf_matrix[num1], tf_idf_matrix[num2])
#             print "euc", euc
#    
#     print "cos",cos4
#     print "len_cos",len(cos4)
#     simLSA = similaridade_lsa(treinamento, lsaUsu, lsaPosIni)
#     print "simLSA"
#     pprint(sorted(simLSA, reverse=True))
#    
#     simLSA1 = similaridade_lsa(posIni, lsaUsu, lsaPosIni)
#     print "simLSA1"
#     pprint(sorted(simLSA1, reverse=True))
#    
#     sum_cos = 0
#     if len(cos4) != 0:
#         for i in cos4:
#             sum_cos = i + sum_cos
#         print "media = ", sum_cos / len(cos4)
#     else:
#         print "sem média"
#   
#   
# #########################################################################################    
#     print "grupo 5", len(grupo5)
#     cos5 = []
#     lsaPosIni = []
#     lsaUsu =[]
#     print lsaPosIni
#     print lsaUsu
#    
#     for y in range(len(ind_aux5)):
#         lsaPosIni.append(posIni[ind_aux5[y]])
#         lsaUsu.append(aux_usu[ind_aux5[y]])
#         for x in range(y+1, len(ind_aux5)):
#             num1 = ind_aux5[y]
#             num2 = ind_aux5[x]
#             cos5.append(cosine_similarity(tf_idf_matrix[num1], tf_idf_matrix[num2]))
#             euc = euclidean_distances(tf_idf_matrix[num1], tf_idf_matrix[num2],squared=True)
#             print aux_usu[num1],aux_usu[num2]
#             print "cosine", cosine_similarity(tf_idf_matrix[num1], tf_idf_matrix[num2])
#             print "euc", euc
#    
#     print "cos",cos5
#     print "len_cos", len(cos5)
#     simLSA = similaridade_lsa(treinamento, lsaUsu, lsaPosIni)
#     print "simLSA"
#     pprint(sorted(simLSA, reverse=True))
#    
#     simLSA1 = similaridade_lsa(posIni, lsaUsu, lsaPosIni)
#     print "simLSA1"
#     pprint(sorted(simLSA1, reverse=True))
#    
#     sum_cos = 0
#     if len(cos5) != 0:
#         for i in cos5:
#             sum_cos = i + sum_cos
#         print "media = ", sum_cos / len(cos5)
#     else:
#         print "sem média"
#   
# #########################################################################################
#     print "grupo 6", len(grupo6)
#     cos6 = []
#     lsaPosIni = []
#     lsaUsu =[]
#    
#     for y in range(len(ind_aux6)):
#         lsaPosIni.append(posIni[ind_aux6[y]])
#         lsaUsu.append(aux_usu[ind_aux6[y]])
#         for x in range(y+1, len(ind_aux6)):
#             num1 = ind_aux6[y]
#             num2 = ind_aux6[x]
#             cos6.append(cosine_similarity(tf_idf_matrix[num1], tf_idf_matrix[num2]))
#             euc = euclidean_distances(tf_idf_matrix[num1], tf_idf_matrix[num2],squared=True)
#             print aux_usu[num1],aux_usu[num2]
#             print "cosine", cosine_similarity(tf_idf_matrix[num1], tf_idf_matrix[num2])
#             print "euc", euc
#    
#     print "cos",cos6
#     print "len_cos",len(cos6)
#     simLSA = similaridade_lsa(treinamento, lsaUsu, lsaPosIni)
#     print "simLSA"
#     pprint(sorted(simLSA, reverse=True))
#    
#     simLSA1 = similaridade_lsa(posIni, lsaUsu, lsaPosIni)
#     print "simLSA1"
#     pprint(sorted(simLSA1, reverse=True))
#    
#     sum_cos = 0
#     if len(cos6) != 0:
#         for i in cos6:
#             sum_cos = i + sum_cos
#         print "media = ", sum_cos / len(cos6)
#     else:
#         print "sem média"
 
     
##########################################################################################
    fim = datetime.now()
    print fim,"gruposArgumentacao"
    
    duration = time.time() - start
    stats = yappi.get_func_stats()
    stats.save('gruposArgumentacao.out', type = 'callgrind')
    
    return grupo1, grupo2, grupo3, grupo4, grupo5, grupo6, tese