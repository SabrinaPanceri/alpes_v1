#coding: utf-8
 
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances
from sklearn.feature_extraction.text import CountVectorizer
from alpes_core.ex_kmeans import tfIdf_Kmeans
from alpes_core.ex_lsa import similaridade_lsa
from alpes_core.textProcess import removeA, removePontuacao, removeStopWords, similaridadeCossenos
import codecs
from pprint import pprint
from alpes_core.lsa_kmeans import LSA_Kmeans
import os
 
def clusters(auxResult, numCluster=6, lsa_km=True, tfIdf_km=False, treino_externo=True):
 
##########################################################################################
#                                    VARIÁVEIS                                           #
##########################################################################################
     
    st_tese = auxResult[0]
    posIni = [removeA(removePontuacao(i)) for i in auxResult[1]]
    sw_tese = auxResult[2]
    aux_usu = auxResult[3]
    st_posInicial = auxResult[4]
    tese = [removeA(removePontuacao(i)) for i in auxResult[5]]
    sw_posIni = [removeStopWords(i) for i in auxResult[1]]
     
    grupos = []
    grupo1 = []
    grupo2 = []
    grupo3 = []
    grupo4 = []
    grupo5 = []
    grupo6 = []
    indices = []
     
     
##########################################################################################
     
    #ABORDAGEM 1 -> COM LSA E KMEANS JUNTOS
    if lsa_km == True:
        #BASE DE TREINAMENTO COMPOSTA POR TEXTOS EXTERNOS - MATERIAL DIDÁTICO
        if treino_externo == True:
            base_treinamento = codecs.open(os.path.join(os.path.dirname(__file__),'../arquivos/baseTreinamento.txt'), 'r', 'UTF8')
            treinamento = [removeA(removePontuacao(i)) for i in base_treinamento]
            base_treinamento.close()
             
            if numCluster == 3:
                grupos = LSA_Kmeans(clusters=3, textoTreinamento=treinamento, nomeUsuarios=aux_usu, textoComparacao=posIni)
            if numCluster == 4:
                grupos = LSA_Kmeans(clusters=4, textoTreinamento=treinamento, nomeUsuarios=aux_usu, textoComparacao=posIni)
            if numCluster == 5:
                grupos = LSA_Kmeans(clusters=5, textoTreinamento=treinamento, nomeUsuarios=aux_usu, textoComparacao=posIni)
            if numCluster == 6:
                grupos = LSA_Kmeans(clusters=6, textoTreinamento=treinamento, nomeUsuarios=aux_usu, textoComparacao=posIni)
 
        #BASE DE TREINAMENTO COMPOSTA PELO POSIC. INICIAL
        else:
            if numCluster == 3:
                grupos = LSA_Kmeans(clusters=3, textoTreinamento=posIni, nomeUsuarios=aux_usu, textoComparacao=posIni)
            if numCluster == 4:
                grupos = LSA_Kmeans(clusters=4, textoTreinamento=posIni, nomeUsuarios=aux_usu, textoComparacao=posIni)
            if numCluster == 5:
                grupos = LSA_Kmeans(clusters=5, textoTreinamento=posIni, nomeUsuarios=aux_usu, textoComparacao=posIni)
            if numCluster == 6:
                grupos = LSA_Kmeans(clusters=6, textoTreinamento=posIni, nomeUsuarios=aux_usu, textoComparacao=posIni)
 
##########################################################################################
 
    #ABORDAGEM 2 -> Clusterização utilizando Tf-IDF e K-Means    
    if tfIdf_km == True:
         
        if numCluster == 3:
            grupos = tfIdf_Kmeans(st_posInicial, 3)
        if numCluster == 4:
            grupos = tfIdf_Kmeans(st_posInicial, 4)
        if numCluster == 5:
            grupos = tfIdf_Kmeans(st_posInicial, 5)
        if numCluster == 6:
            grupos = tfIdf_Kmeans(st_posInicial, 6)
         
     
    ##########################################################################################
    #                            SEPARAÇÃO DOS AGRUPAMENTOS                                  #
    ##########################################################################################
 
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
            elif i == 3:
                aux = grupos[i][j]
                texto = "Aluno:"+ aux_usu[aux] + " => Posicionamento Inicial: " +  posIni[aux]
                grupo4.append(texto)
                indices.append(grupos[i][j])
            elif i == 4:
                aux = grupos[i][j]
                texto = "Aluno:"+ aux_usu[aux] + " => Posicionamento Inicial: " +  posIni[aux]
                grupo5.append(texto)
                indices.append(grupos[i][j])
            elif i == 5:
                aux = grupos[i][j]
                texto = "Aluno:"+ aux_usu[aux] + " => Posicionamento Inicial: " +  posIni[aux]
                grupo6.append(texto)
                indices.append(grupos[i][j])
     
    ##########################################################################################
    #                          IMPRESSÃO DOS AGRUPAMENTOS                                    #
    ##########################################################################################
    transformer = TfidfTransformer()
    tfIdf = transformer.fit_transform(posIni)
     
     
     
     
    ##########################################################################################
            
    if numCluster == 3:
    #PARA 3 CLUSTERS
        ind_aux = indices[:len(grupo1)]
        ind_aux2 = indices[len(ind_aux):len(ind_aux)+len(grupo2)]
        ind_aux3 = indices[len(ind_aux)+len(grupo2):]
             
        print "grupo 1", len(grupo1)
        cos = []
     
        for y in range(len(ind_aux)):
            for x in range(y+1, len(ind_aux)):
                num1 = ind_aux[y]
                num2 = ind_aux[x]
                cos.append(similaridadeCossenos(sw_posIni[num1].__str__(),sw_posIni[num2].__str__()))
        print cos
     
        sum_cos = 0
     
        if len(cos) != 0:
            for i in cos:
                sum_cos = i + sum_cos
     
            print "media = ", sum_cos / len(cos)
        else:
            print "sem média"
     
    ##########################################################################################
        print "grupo 2", len(grupo2)
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
                cos2.append(cosine_similarity(vectorizer[num1], vectorizer[num2]))
#                 euc = euclidean_distances(tf_idf_matrix[num1], tf_idf_matrix[num2],squared=True)
#     #             print aux_usu[num1],aux_usu[num2]
#                 print "cosine", cosine_similarity(tf_idf_matrix[num1], tf_idf_matrix[num2])
#                 print "euc", euc
        print "cos",cos2
        print "len_cos",len(cos2)
        simLSA = similaridade_lsa(treinamento, lsaUsu, lsaPosIni)
        print "simLSA"
        pprint(sorted(simLSA, reverse=True))
     
        simLSA1 = similaridade_lsa(posIni, lsaUsu, lsaPosIni)
        print "simLSA1"
        pprint(sorted(simLSA1, reverse=True))
     
     
        sum_cos = 0
        if len(cos2) != 0:
            for i in cos2:
                sum_cos = i + sum_cos
            print "media = ", sum_cos / len(cos2)
        else:
            print "sem média"
     
    ##########################################################################################    
        print "grupo 3", len(grupo3)
        cos3 = []    
        lsaPosIni = []
        lsaUsu =[]
        print lsaPosIni
        print lsaUsu
     
        for y in range(len(ind_aux3)):
            lsaPosIni.append(posIni[ind_aux3[y]])
            lsaUsu.append(aux_usu[ind_aux3[y]])
            for x in range(y+1, len(ind_aux3)):
                num1 = ind_aux3[y]
                num2 = ind_aux3[x]
                cos3.append(cosine_similarity(vectorizer[num1], vectorizer[num2]))
#                 euc = euclidean_distances(tf_idf_matrix[num1], tf_idf_matrix[num2],squared=True)
#     #             print aux_usu[num1],aux_usu[num2]
#                 print "cosine", cosine_similarity(tf_idf_matrix[num1], tf_idf_matrix[num2])
#                 print "euc", euc
     
        print "cos",cos3
        print "len_cos",len(cos3)
     
        simLSA = similaridade_lsa(treinamento, lsaUsu, lsaPosIni)
        print "simLSA"
        pprint(sorted(simLSA, reverse=True))
     
        simLSA1 = similaridade_lsa(posIni, lsaUsu, lsaPosIni)
        print "simLSA1"
        pprint(sorted(simLSA1, reverse=True))
     
        sum_cos = 0
        if len(cos3) != 0:
            for i in cos3:
                sum_cos = i + sum_cos
            print "media = ", sum_cos / len(cos3)
        else:
            print "sem média"
     
    ##########################################################################################
         
     
    if numCluster == 4:
    #PARA 4 CLUSTERS        
        ind_aux = indices[:len(grupo1)]
        ind_aux2 = indices[len(grupo1):len(grupo1)+len(grupo2)]
        ind_aux3 = indices[len(grupo1)+len(grupo2):(len(grupo1)+len(grupo2))+len(grupo3)]
        ind_aux4 = indices[(len(grupo1)+len(grupo2))+len(grupo3):]
     
        print "grupo 1", len(grupo1)
        cos = []
        lsaPosIni = []
        lsaUsu =[]
     
        for y in range(len(ind_aux)):
    #         print "posIni[y]", aux_usu[ind_aux[y]],posIni[ind_aux[y]]
            lsaPosIni.append(posIni[ind_aux[y]])
            lsaUsu.append(aux_usu[ind_aux[y]])
            for x in range(y+1, len(ind_aux)):
                num1 = ind_aux[y]
                num2 = ind_aux[x]
                cos.append(cosine_similarity(vectorizer[num1], vectorizer[num2]))
#                 euc = euclidean_distances(tf_idf_matrix[num1], tf_idf_matrix[num2],squared=True)
#                 print "cosine", cosine_similarity(tf_idf_matrix[num1], tf_idf_matrix[num2])
#                 print "euc", euc
     
        simLSA = similaridade_lsa(treinamento, lsaUsu, lsaPosIni)
        print "simLSA"
        pprint(sorted(simLSA, reverse=True))
     
        simLSA1 = similaridade_lsa(posIni, lsaUsu, lsaPosIni)
        print "simLSA1"
        pprint(sorted(simLSA1, reverse=True))
        print "cos",cos
        print "len_cos",len(cos)
        sum_cos = 0
     
        if len(cos) != 0:
            for i in cos:
                sum_cos = i + sum_cos
     
            print "media = ", sum_cos / len(cos)
        else:
            print "sem média"
     
    ##########################################################################################
        print "grupo 2", len(grupo2)
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
                cos2.append(cosine_similarity(vectorizer[num1], vectorizer[num2]))
#                 euc = euclidean_distances(tf_idf_matrix[num1], tf_idf_matrix[num2],squared=True)
#     #             print aux_usu[num1],aux_usu[num2]
#                 print "cosine", cosine_similarity(tf_idf_matrix[num1], tf_idf_matrix[num2])
#                 print "euc", euc
        print "cos",cos2
        print "len_cos",len(cos2)
        simLSA = similaridade_lsa(treinamento, lsaUsu, lsaPosIni)
        print "simLSA"
        pprint(sorted(simLSA, reverse=True))
     
        simLSA1 = similaridade_lsa(posIni, lsaUsu, lsaPosIni)
        print "simLSA1"
        pprint(sorted(simLSA1, reverse=True))
     
     
        sum_cos = 0
        if len(cos2) != 0:
            for i in cos2:
                sum_cos = i + sum_cos
            print "media = ", sum_cos / len(cos2)
        else:
            print "sem média"
     
    ##########################################################################################    
        print "grupo 3", len(grupo3)
        cos3 = []    
        lsaPosIni = []
        lsaUsu =[]
        print lsaPosIni
        print lsaUsu
     
        for y in range(len(ind_aux3)):
            lsaPosIni.append(posIni[ind_aux3[y]])
            lsaUsu.append(aux_usu[ind_aux3[y]])
            for x in range(y+1, len(ind_aux3)):
                num1 = ind_aux3[y]
                num2 = ind_aux3[x]
                cos3.append(cosine_similarity(vectorizer[num1], vectorizer[num2]))
#                 euc = euclidean_distances(tf_idf_matrix[num1], tf_idf_matrix[num2],squared=True)
#     #             print aux_usu[num1],aux_usu[num2]
#                 print "cosine", cosine_similarity(tf_idf_matrix[num1], tf_idf_matrix[num2])
#                 print "euc", euc
     
        print "cos",cos3
        print "len_cos",len(cos3)
     
        simLSA = similaridade_lsa(treinamento, lsaUsu, lsaPosIni)
        print "simLSA"
        pprint(sorted(simLSA, reverse=True))
     
        simLSA1 = similaridade_lsa(posIni, lsaUsu, lsaPosIni)
        print "simLSA1"
        pprint(sorted(simLSA1, reverse=True))
     
        sum_cos = 0
        if len(cos3) != 0:
            for i in cos3:
                sum_cos = i + sum_cos
            print "media = ", sum_cos / len(cos3)
        else:
            print "sem média"
     
    ##########################################################################################
        print "grupo 4", len(grupo4)
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
                cos4.append(cosine_similarity(vectorizer[num1], vectorizer[num2]))
#                 euc = euclidean_distances(tf_idf_matrix[num1], tf_idf_matrix[num2],squared=True)
#     #             print aux_usu[num1],aux_usu[num2]
#                 print "cosine", cosine_similarity(tf_idf_matrix[num1], tf_idf_matrix[num2])
#                 print "euc", euc
      
        print "cos",cos4
        print "len_cos",len(cos4)
        simLSA = similaridade_lsa(treinamento, lsaUsu, lsaPosIni)
        print "simLSA"
        pprint(sorted(simLSA, reverse=True))
      
        simLSA1 = similaridade_lsa(posIni, lsaUsu, lsaPosIni)
        print "simLSA1"
        pprint(sorted(simLSA1, reverse=True))
      
        sum_cos = 0
        if len(cos4) != 0:
            for i in cos4:
                sum_cos = i + sum_cos
            print "media = ", sum_cos / len(cos4)
        else:
            print "sem média"
 
    if numCluster == 5:
    #PARA 5 CLUSTERS        
        ind_aux = indices[:len(grupo1)]
        ind_aux2 = indices[len(grupo1):len(grupo1)+len(grupo2)]
        ind_aux3 = indices[len(grupo1)+len(grupo2):(len(grupo1)+len(grupo2))+len(grupo3)]
        ind_aux4 = indices[(len(grupo1)+len(grupo2)+len(grupo3)):(len(grupo1)+len(grupo2)+len(grupo3))+len(grupo4)]
        ind_aux5 = indices[(len(grupo1)+len(grupo2)+len(grupo3))+len(grupo4):]
 
        ##########################################################################################
        #                                AGRUPAMENTOS                                            #
        ##########################################################################################
 
        print "grupo 1", len(grupo1)
        cos = []
        lsaPosIni = []
        lsaUsu =[]
     
        for y in range(len(ind_aux)):
    #         print "posIni[y]", aux_usu[ind_aux[y]],posIni[ind_aux[y]]
            lsaPosIni.append(posIni[ind_aux[y]])
            lsaUsu.append(aux_usu[ind_aux[y]])
            for x in range(y+1, len(ind_aux)):
                num1 = ind_aux[y]
                num2 = ind_aux[x]
                cos.append(cosine_similarity(vectorizer[num1], vectorizer[num2]))
#                 euc = euclidean_distances(tf_idf_matrix[num1], tf_idf_matrix[num2],squared=True)
#                 print "cosine", cosine_similarity(tf_idf_matrix[num1], tf_idf_matrix[num2])
#                 print "euc", euc
     
        simLSA = similaridade_lsa(treinamento, lsaUsu, lsaPosIni)
        print "simLSA"
        pprint(sorted(simLSA, reverse=True))
     
        simLSA1 = similaridade_lsa(posIni, lsaUsu, lsaPosIni)
        print "simLSA1"
        pprint(sorted(simLSA1, reverse=True))
        print "cos",cos
        print "len_cos",len(cos)
        sum_cos = 0
     
        if len(cos) != 0:
            for i in cos:
                sum_cos = i + sum_cos
     
            print "media = ", sum_cos / len(cos)
        else:
            print "sem média"
     
    ##########################################################################################
        print "grupo 2", len(grupo2)
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
                cos2.append(cosine_similarity(vectorizer[num1], vectorizer[num2]))
#                 euc = euclidean_distances(tf_idf_matrix[num1], tf_idf_matrix[num2],squared=True)
#     #             print aux_usu[num1],aux_usu[num2]
#                 print "cosine", cosine_similarity(tf_idf_matrix[num1], tf_idf_matrix[num2])
#                 print "euc", euc
        print "cos",cos2
        print "len_cos",len(cos2)
        simLSA = similaridade_lsa(treinamento, lsaUsu, lsaPosIni)
        print "simLSA"
        pprint(sorted(simLSA, reverse=True))
     
        simLSA1 = similaridade_lsa(posIni, lsaUsu, lsaPosIni)
        print "simLSA1"
        pprint(sorted(simLSA1, reverse=True))
     
     
        sum_cos = 0
        if len(cos2) != 0:
            for i in cos2:
                sum_cos = i + sum_cos
            print "media = ", sum_cos / len(cos2)
        else:
            print "sem média"
     
    ##########################################################################################    
        print "grupo 3", len(grupo3)
        cos3 = []    
        lsaPosIni = []
        lsaUsu =[]
        print lsaPosIni
        print lsaUsu
     
        for y in range(len(ind_aux3)):
            lsaPosIni.append(posIni[ind_aux3[y]])
            lsaUsu.append(aux_usu[ind_aux3[y]])
            for x in range(y+1, len(ind_aux3)):
                num1 = ind_aux3[y]
                num2 = ind_aux3[x]
                cos3.append(cosine_similarity(vectorizer[num1], vectorizer[num2]))
#                 euc = euclidean_distances(tf_idf_matrix[num1], tf_idf_matrix[num2],squared=True)
#     #             print aux_usu[num1],aux_usu[num2]
#                 print "cosine", cosine_similarity(tf_idf_matrix[num1], tf_idf_matrix[num2])
#                 print "euc", euc
     
        print "cos",cos3
        print "len_cos",len(cos3)
     
        simLSA = similaridade_lsa(treinamento, lsaUsu, lsaPosIni)
        print "simLSA"
        pprint(sorted(simLSA, reverse=True))
     
        simLSA1 = similaridade_lsa(posIni, lsaUsu, lsaPosIni)
        print "simLSA1"
        pprint(sorted(simLSA1, reverse=True))
     
        sum_cos = 0
        if len(cos3) != 0:
            for i in cos3:
                sum_cos = i + sum_cos
            print "media = ", sum_cos / len(cos3)
        else:
            print "sem média"
     
    ##########################################################################################
        print "grupo 4", len(grupo4)
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
                cos4.append(cosine_similarity(vectorizer[num1], vectorizer[num2]))
#                 euc = euclidean_distances(tf_idf_matrix[num1], tf_idf_matrix[num2],squared=True)
#     #             print aux_usu[num1],aux_usu[num2]
#                 print "cosine", cosine_similarity(tf_idf_matrix[num1], tf_idf_matrix[num2])
#                 print "euc", euc
      
        print "cos",cos4
        print "len_cos",len(cos4)
        simLSA = similaridade_lsa(treinamento, lsaUsu, lsaPosIni)
        print "simLSA"
        pprint(sorted(simLSA, reverse=True))
      
        simLSA1 = similaridade_lsa(posIni, lsaUsu, lsaPosIni)
        print "simLSA1"
        pprint(sorted(simLSA1, reverse=True))
      
        sum_cos = 0
        if len(cos4) != 0:
            for i in cos4:
                sum_cos = i + sum_cos
            print "media = ", sum_cos / len(cos4)
        else:
            print "sem média"
     
    ##########################################################################################
        print "grupo 5", len(grupo5)
        cos5 = []
        lsaPosIni = []
        lsaUsu =[]
        print lsaPosIni
        print lsaUsu
      
        for y in range(len(ind_aux5)):
            lsaPosIni.append(posIni[ind_aux5[y]])
            lsaUsu.append(aux_usu[ind_aux5[y]])
            for x in range(y+1, len(ind_aux5)):
                num1 = ind_aux5[y]
                num2 = ind_aux5[x]
#                 cos5.append(cosine_similarity(vectorizer[num1], vectorizer[num2]))
#                 euc = euclidean_distances(tf_idf_matrix[num1], tf_idf_matrix[num2],squared=True)
#     #             print aux_usu[num1],aux_usu[num2]
#                 print "cosine", cosine_similarity(tf_idf_matrix[num1], tf_idf_matrix[num2])
#                 print "euc", euc
      
        print "cos",cos5
        print "len_cos", len(cos5)
        simLSA = similaridade_lsa(treinamento, lsaUsu, lsaPosIni)
        print "simLSA"
        pprint(sorted(simLSA, reverse=True))
      
        simLSA1 = similaridade_lsa(posIni, lsaUsu, lsaPosIni)
        print "simLSA1"
        pprint(sorted(simLSA1, reverse=True))
      
        sum_cos = 0
        if len(cos5) != 0:
            for i in cos5:
                sum_cos = i + sum_cos
            print "media = ", sum_cos / len(cos5)
        else:
            print "sem média"
     
    ##########################################################################################
             
 
    if numCluster == 6:
        #PARA 6 CLUSTERS        
        ind_aux = indices[:len(grupo1)]
        ind_aux2 = indices[len(grupo1):len(grupo1)+len(grupo2)]
        ind_aux3 = indices[len(grupo1)+len(grupo2):(len(grupo1)+len(grupo2))+len(grupo3)]
        ind_aux4 = indices[(len(grupo1)+len(grupo2)+len(grupo3)):(len(grupo1)+len(grupo2)+len(grupo3))+len(grupo4)]
        ind_aux5 = indices[(len(grupo1)+len(grupo2)+len(grupo3))+len(grupo4):(len(grupo1)+len(grupo2)+len(grupo3)+len(grupo4))+len(grupo5)]
        ind_aux6 = indices[(len(grupo1)+len(grupo2)+len(grupo3)+len(grupo4))+len(grupo5):]
     
        print "grupo 1", len(grupo1)
        cos = []
        lsaPosIni = []
        lsaUsu =[]
     
        for y in range(len(ind_aux)):
    #         print "posIni[y]", aux_usu[ind_aux[y]],posIni[ind_aux[y]]
            lsaPosIni.append(posIni[ind_aux[y]])
            lsaUsu.append(aux_usu[ind_aux[y]])
            for x in range(y+1, len(ind_aux)):
                num1 = ind_aux[y]
                num2 = ind_aux[x]
                cos.append(cosine_similarity(vectorizer[num1], vectorizer[num2]))
#                 euc = euclidean_distances(tf_idf_matrix[num1], tf_idf_matrix[num2],squared=True)
#                 print "cosine", cosine_similarity(tf_idf_matrix[num1], tf_idf_matrix[num2])
#                 print "euc", euc
     
        simLSA = similaridade_lsa(treinamento, lsaUsu, lsaPosIni)
        print "simLSA"
        pprint(sorted(simLSA, reverse=True))
     
        simLSA1 = similaridade_lsa(posIni, lsaUsu, lsaPosIni)
        print "simLSA1"
        pprint(sorted(simLSA1, reverse=True))
        print "cos",cos
        print "len_cos",len(cos)
        sum_cos = 0
     
        if len(cos) != 0:
            for i in cos:
                sum_cos = i + sum_cos
     
            print "media = ", sum_cos / len(cos)
        else:
            print "sem média"
     
    ##########################################################################################
        print "grupo 2", len(grupo2)
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
                cos2.append(cosine_similarity(vectorizer[num1], vectorizer[num2]))
#                 euc = euclidean_distances(tf_idf_matrix[num1], tf_idf_matrix[num2],squared=True)
#     #             print aux_usu[num1],aux_usu[num2]
#                 print "cosine", cosine_similarity(tf_idf_matrix[num1], tf_idf_matrix[num2])
#                 print "euc", euc
        print "cos",cos2
        print "len_cos",len(cos2)
        simLSA = similaridade_lsa(treinamento, lsaUsu, lsaPosIni)
        print "simLSA"
        pprint(sorted(simLSA, reverse=True))
     
        simLSA1 = similaridade_lsa(posIni, lsaUsu, lsaPosIni)
        print "simLSA1"
        pprint(sorted(simLSA1, reverse=True))
     
     
        sum_cos = 0
        if len(cos2) != 0:
            for i in cos2:
                sum_cos = i + sum_cos
            print "media = ", sum_cos / len(cos2)
        else:
            print "sem média"
     
    ##########################################################################################    
        print "grupo 3", len(grupo3)
        cos3 = []    
        lsaPosIni = []
        lsaUsu =[]
        print lsaPosIni
        print lsaUsu
     
        for y in range(len(ind_aux3)):
            lsaPosIni.append(posIni[ind_aux3[y]])
            lsaUsu.append(aux_usu[ind_aux3[y]])
            for x in range(y+1, len(ind_aux3)):
                num1 = ind_aux3[y]
                num2 = ind_aux3[x]
                cos3.append(cosine_similarity(vectorizer[num1], vectorizer[num2]))
#                 euc = euclidean_distances(tf_idf_matrix[num1], tf_idf_matrix[num2],squared=True)
#     #             print aux_usu[num1],aux_usu[num2]
#                 print "cosine", cosine_similarity(tf_idf_matrix[num1], tf_idf_matrix[num2])
#                 print "euc", euc
     
        print "cos",cos3
        print "len_cos",len(cos3)
     
        simLSA = similaridade_lsa(treinamento, lsaUsu, lsaPosIni)
        print "simLSA"
        pprint(sorted(simLSA, reverse=True))
     
        simLSA1 = similaridade_lsa(posIni, lsaUsu, lsaPosIni)
        print "simLSA1"
        pprint(sorted(simLSA1, reverse=True))
     
        sum_cos = 0
        if len(cos3) != 0:
            for i in cos3:
                sum_cos = i + sum_cos
            print "media = ", sum_cos / len(cos3)
        else:
            print "sem média"
     
    ##########################################################################################
        print "grupo 4", len(grupo4)
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
                cos4.append(cosine_similarity(vectorizer[num1], vectorizer[num2]))
#                 euc = euclidean_distances(tf_idf_matrix[num1], tf_idf_matrix[num2],squared=True)
#     #             print aux_usu[num1],aux_usu[num2]
#                 print "cosine", cosine_similarity(tf_idf_matrix[num1], tf_idf_matrix[num2])
#                 print "euc", euc
      
        print "cos",cos4
        print "len_cos",len(cos4)
        simLSA = similaridade_lsa(treinamento, lsaUsu, lsaPosIni)
        print "simLSA"
        pprint(sorted(simLSA, reverse=True))
      
        simLSA1 = similaridade_lsa(posIni, lsaUsu, lsaPosIni)
        print "simLSA1"
        pprint(sorted(simLSA1, reverse=True))
      
        sum_cos = 0
        if len(cos4) != 0:
            for i in cos4:
                sum_cos = i + sum_cos
            print "media = ", sum_cos / len(cos4)
        else:
            print "sem média"
     
    ##########################################################################################
        print "grupo 5", len(grupo5)
        cos5 = []
        lsaPosIni = []
        lsaUsu =[]
        print lsaPosIni
        print lsaUsu
      
        for y in range(len(ind_aux5)):
            lsaPosIni.append(posIni[ind_aux5[y]])
            lsaUsu.append(aux_usu[ind_aux5[y]])
            for x in range(y+1, len(ind_aux5)):
                num1 = ind_aux5[y]
                num2 = ind_aux5[x]
                cos5.append(cosine_similarity(vectorizer[num1], vectorizer[num2]))
#                 euc = euclidean_distances(tf_idf_matrix[num1], tf_idf_matrix[num2],squared=True)
#     #             print aux_usu[num1],aux_usu[num2]
#                 print "cosine", cosine_similarity(tf_idf_matrix[num1], tf_idf_matrix[num2])
#                 print "euc", euc
      
        print "cos",cos5
        print "len_cos", len(cos5)
        simLSA = similaridade_lsa(treinamento, lsaUsu, lsaPosIni)
        print "simLSA"
        pprint(sorted(simLSA, reverse=True))
      
        simLSA1 = similaridade_lsa(posIni, lsaUsu, lsaPosIni)
        print "simLSA1"
        pprint(sorted(simLSA1, reverse=True))
      
        sum_cos = 0
        if len(cos5) != 0:
            for i in cos5:
                sum_cos = i + sum_cos
            print "media = ", sum_cos / len(cos5)
        else:
            print "sem média"
     
    ##########################################################################################    
     
        print "grupo 6", len(grupo6)
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
                cos6.append(cosine_similarity(vectorizer[num1], vectorizer[num2]))
#                 euc = euclidean_distances(tf_idf_matrix[num1], tf_idf_matrix[num2],squared=True)
#     #             print aux_usu[num1],aux_usu[num2]
#                 print "cosine", cosine_similarity(tf_idf_matrix[num1], tf_idf_matrix[num2])
#                 print "euc", euc
      
        print "cos",cos6
        print "len_cos",len(cos6)
        simLSA = similaridade_lsa(treinamento, lsaUsu, lsaPosIni)
        print "simLSA"
        pprint(sorted(simLSA, reverse=True))
      
        simLSA1 = similaridade_lsa(posIni, lsaUsu, lsaPosIni)
        print "simLSA1"
        pprint(sorted(simLSA1, reverse=True))
      
        sum_cos = 0
        if len(cos6) != 0:
            for i in cos6:
                sum_cos = i + sum_cos
            print "media = ", sum_cos / len(cos6)
        else:
            print "sem média"
 
 
##########################################################################################
    return grupo1, grupo2, grupo3, grupo4, grupo5, grupo6, tese
