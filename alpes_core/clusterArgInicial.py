# -*- coding: utf-8 -*-
#############################################################################################################
# Imports necessários
import HTMLParser
import re, nltk
from django.db import connection
from alpes_core.textProcess import removeStopWords, stemming
from nltk.stem import RSLPStemmer
from nltk.corpus import floresta
from nltk.probability import FreqDist


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
## 6 - Normalização (falta desenv)                                                                          #
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
    
    #lista com dados após a remoção das stopwords
    sw_tese = []
    sw_posInicial = []
    aux_usu = []

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
            

    #Colocando os textos de posicionamento final em numa lista separada
    for i in dados:
        x = 0
        usu.append(i[x].upper())
        posInicial.append(i[x+1].lower()) #lista com o posicionamento Inicial

#############################################################################################################
#Fases de pré-processamento linguistico
# - Remoção de stopwords
# - Troca de caracteres acentuados por caracteres não acentuados
# - Remoção pontuações
    for i in usu:
        aux_usu.append(removeStopWords(i))

    for i in tese:
        sw_tese.append(removeStopWords(i))


    for i in posInicial:
        sw_posInicial.append(removeStopWords(i))

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
# Normalização dos termos
# Troca de termos similares por um mesmo termo para auxiliar no cálculo de similaridade
# Experimentos com o Floresta Treebank
# print floresta.words()
# 
# print floresta.tagged_words()
# 
# def simplify_tag(t):
#     if "+" in t:
#         return t[t.index("+")+1:]
#     else:
#         return t
#      
# twords = floresta.tagged_words()
# twords = [(w.lower(), simplify_tag(t)) for (w,t) in twords]
# print twords[:10]
# 
# print(' '.join(word + '/' + tag for (word, tag) in twords[:10]))
# 
# tags = [simplify_tag(tag) for (word,tag) in floresta.tagged_words()]
# fd = FreqDist(tags)
# print fd.keys()[:20]
# 
# psents = floresta.parsed_sents()
# print floresta.tagged_sents()



    
