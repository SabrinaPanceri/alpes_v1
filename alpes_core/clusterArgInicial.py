# -*- coding: utf-8 -*-
#############################################################################################################

# Imports obrigatorios
import HTMLParser
import re
import nlpnet
from django.db import connection
from alpes_core.textProcess import removeStopWords, removePontuacao, limpaCorpus
from nltk.stem import RSLPStemmer
from alpes_core.wordnet import normalizacao


# import nltk, sys
# from alpes_core.textProcess import stemming
# from nltk.corpus import floresta
# from nltk.probability import FreqDist
# from nltk import word_tokenize as wt


#############################################################################################################
### INDICA A BASE DE DADOS PARA FAZER A CLASSIFICACAO SINTATICA
### USO DO POS TAGGER DA NLPNET 
### COPIAR PARA O SERVIDOR A PASTA NLPNET-DATA
### COLOCAR CAMINHO CORRETO DENTRO DO SERVIDOR!!!
#nlpnet.set_data_dir('/home/panceri/nlpnet-data/pos-pt')
nlpnet.set_data_dir('/home/panceri/nlpnet-data/')

#############################################################################################################

#############################################################################################################

#############################################################################################################
## Desenvolvimento da lógica de execução do Núcleo de processamento do Alpes                                #
## Aplicação das técnicas de pré-processamento textual a fim de ajudar no processo de comparação e busca    #
## de textos similares                                                                                      #
## Técnicas desenvolvidas                                                                                   #
## 1 - Case folding                                                                                         #
## 2 - Troca de caracteres acentuados por caracteres não acentuados                                         #
## 3 - Remoção pontuações                                                                                   #
## 4 - Remoção de stopwords                                                                                 #
## 5 - Stemming                                                                                             #
## 6 - Normalização (em desenvolvimento)                                                                          #
#############################################################################################################

##############################################################################################################
## DESENVOLVIMENTO DA FERRAMENTA "GRUPOS DE ARGUMENTAÇÃO" - ARTIGO SBIE 2015
## UTILIZAÇÃO DO POSICIONAMENTO INICIAL PARA CRIAR GRUPOS DE ALUNOS QUE INICIARAM O DEBATE COM CONHECIMENTOS 
## SIMILARES SOBRE A TESE 
##############################################################################################################  

def clusterArgInicial(idtese):
    #Variaveis e funçoes para conexação com o banco de dados do Debate de Teses
    cursor = connection.cursor()
    cursor2 = connection.cursor()

    cursor.execute("select distinct `usr`.`primeironome` as `name`, `arg`.`argumento` AS `posicionamentoinicial` from ((((`argumento` `arg` join `revisao` `rev`) join `replica` `rep`) join `posicionamento` `pos`) join `argumentador` `urg`)join `usuario` `usr`  where ((`arg`.`tese_idtese` = " + idtese + "  ) and (`rev`.`argumento_idargumento` = `arg`.`idargumento`) and (`rep`.`revisao_idrevisao` = `rev`.`idrevisao`) and (`arg`.`argumentador_idargumentador` = `pos`.`argumentador_idargumentador`) and (`arg`.`tese_idtese` = `pos`.`tese_idtese`) and (`arg`.`posicionamentoinicial` is not null) and (`arg`.`argumentador_idargumentador` = `urg`.`idargumentador`) and(`urg`.`usuario_idusuario` = `usr`.`idusuario`) and (`pos`.`posicionamentofinal` is not null))")
    cursor2.execute("select tese from tese where idtese="+ idtese)
    
    #Variavel e função para tratar tags html e acentos com codificação ISO
    h = HTMLParser.HTMLParser()
    
    #dados retirados da consulta ao banco
    dadosSql = cursor.fetchall()
    textotese = cursor2.fetchall()
    
    #listas para tratar os dados iniciais
    usu = []
    posInicial = []
    dados = []
    tese = []
    
    #lista com dados pos tagger
    tag_posInicial = []
    
    #lista com dados após a remoção das stopwords
    sw_tese = []
    sw_posInicial = []
    aux_usu = []
    sw_tagPosInicial = [] #texto marcado e sem stopwords

    #lista com dados após a aplicação de Stemming
    st_posInicial = []
    st_tese = []
      

#############################################################################################################    
#Aplicacao de Case Folding
    for d in dadosSql:
        dados.append([re.sub('<[^>]*>', '', h.unescape(d[0])).lower(),
                      re.sub('<[^>]*>', '', h.unescape(d[1])).lower()])

    for t in textotese:
        tese.append(re.sub('<[^>]*>', '', h.unescape(t[0])).lower())
            

    #Colocando os textos de posicionamento inicial em numa lista separada
    for i in dados:
        x = 0
        usu.append(i[x].upper())
        posInicial.append(i[x+1].lower()) #lista com o posicionamento Inicial

#############################################################################################################
### Classificacao das palavras de acordo com sua classe gramatical
### Utilizacao do postagger NLPNET
### http://nilc.icmc.usp.br/nlpnet/index.html#
    
    tagger = nlpnet.POSTagger()
    
    semAce_posInicial = [] #armazena o posInicial apenas sem acentos e sem pontuacao
    
    for i in posInicial:
        #semAce_posInicial.append(removeA(removePontuacao(i)))
        semAce_posInicial.append(removePontuacao(i))
    
    for i in semAce_posInicial:
        tag_posInicial.append(tagger.tag(i))
    
#############################################################################################################
### Semantic Role Labeling model 
### http://www.nilc.icmc.usp.br/nlpnet/models.html#srl-portuguese
### Marcacao semantica funcionando. Verificar como usar para melhorar os resultados.
#     srl_tagger = nlpnet.SRLTagger()
#     auxSrl_PosIni = [] 
#     srl_PosIni = [] #posicionamento inicial tagueado com SRL 
#     
#     for i in posInicial:
#         auxSrl_PosIni.append(srl_tagger.tag(i))
#       
#     for aux in auxSrl_PosIni:
#         for j in aux:
#             srl_PosIni.append(j.arg_structures)

#############################################################################################################
### REMOCAO DE STOPWORDS
### Remocao dos termos de acordo com a NLTK
    
    for i in usu:
        aux_usu.append(removeStopWords(i))

    for i in tese:
        sw_tese.append(removeStopWords(i))

    for i in posInicial:
        sw_posInicial.append(removeStopWords(i))
        
    for i in tag_posInicial:
        sw_tagPosInicial.append(limpaCorpus(i))
        

#############################################################################################################
# Normalização dos termos
# Troca de termos por seus sinonimos com base na WordNet.BR
# http://143.107.183.175:21480/tep2/index.htm

#CONTINUAR DAQUI
    #pela tague pegar a palavra e mandar para normalizacao

#     for i in range(len(tag_posInicial)):
#         for j in range(len(tag_posInicial[i])):
#             for x in tag_posInicial[i][j]:
#                 #print x, "x"
#                 #print x[1], "x[1]"
#                 #print i, "i"
#                 #print j, "j"
#                 
#                 ## Excluir: ART, NUM, 
#                 
#                 if x[1] != "ART":
#                  #   print x[0],"x[0]"
#                     normalizacao(x[0])

    dicSin = {}

    for texto in sw_tagPosInicial:
        #print len(texto)
        for termo in texto:
            normalizacao(dicSin,termo[0], termo[1])
    
    print "dicSin", dicSin
        

#############################################################################################################
#Aplicação do RSPL Stemmer para remoção dos afixos das palavras da lingua portuguesa
#retirando afixos dos textos do posInicial e tese
    stemmer = RSLPStemmer()
 
    for i in range(len(sw_posInicial)):
        st_aux = sw_posInicial[i]
        string_aux = ""
        for sufixo in st_aux.split():
            string_aux = string_aux + " " + stemmer.stem(sufixo)
         
        st_posInicial.append(string_aux)
 
    for i in range(len(sw_tese)):
        st_aux = sw_tese[i]
        string_aux = ""
        for sufixo in st_aux.split():
            string_aux = string_aux + " " + stemmer.stem(sufixo)
         
        st_tese.append(string_aux)


#############################################################################################################
# #LSI
#     lsi_posInicial = []
#     for i in range(len(sw_posInicial)):
#         aux = "posIni(%d): %s" %(i, sw_posInicial[i])
#         lsi_posInicial.append(aux)
# 
# 
#     lsi = gensim.models.lsimodel.LsiModel(lsi_posInicial)
# # #     print sw_posInicial
#     lsi.print_topics(10)



#############################################################################################################
#retorno da função - usado na views.py para alimentar o template debate.html
#passar parametros que devem ser apresentados na templates debate.html
    return [st_tese, posInicial, sw_tese, aux_usu, st_posInicial, tese]


#############################################################################################################












  
