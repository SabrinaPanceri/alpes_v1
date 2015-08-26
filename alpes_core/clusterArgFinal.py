# -*- coding: utf-8 -*-
#############################################################################################################
# Imports necessários
import HTMLParser
import re
# import nltk
from django.db import connection
from alpes_core.textProcess import removeStopWords
from nltk.stem import RSLPStemmer
# from nltk.corpus import floresta
# from nltk.probability import FreqDist



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
## DESENVOLVIMENTO DA FERRAMENTA "GRUPOS DE ARGUMENTAÇÃO" - ARTIGO SBIE 2014
## UTILIZAÇÃO DO POSICIONAMENTO FINAL PARA CRIAR GRUPOS DE ALUNOS QUE CHEGARAM A CONCLUSÕES SIMILARES
## AO FINAL DAS INTERAÇÕES DA APDT 
##############################################################################################################  

def clusterArgFinal(idtese):
    #Variaveis e funçoes para conexação com o banco de dados do Debate de Teses
    cursor = connection.cursor()
    cursor2 = connection.cursor()

    cursor.execute("select distinct `usr`.`primeironome` as `name`, `pos`.`posicionamentofinal` AS `posicionamentofinal` from ((((`argumento` `arg` join `revisao` `rev`) join `replica` `rep`) join `posicionamento` `pos`) join `argumentador` `urg`)join `usuario` `usr`  where ((`arg`.`tese_idtese` = " + idtese + "  ) and (`rev`.`argumento_idargumento` = `arg`.`idargumento`) and (`rep`.`revisao_idrevisao` = `rev`.`idrevisao`) and (`arg`.`argumentador_idargumentador` = `pos`.`argumentador_idargumentador`) and (`arg`.`tese_idtese` = `pos`.`tese_idtese`) and (`arg`.`posicionamentoinicial` is not null) and (`arg`.`argumentador_idargumentador` = `urg`.`idargumentador`) and(`urg`.`usuario_idusuario` = `usr`.`idusuario`) and (`pos`.`posicionamentofinal` is not null))")
    cursor2.execute("select tese from tese where grupo_idgrupo = 1064 ")
    
    #Variavel e função para tratar tags html e acentos com codificação ISO
    h = HTMLParser.HTMLParser()
    
    #dados retirados da consulta ao banco
    dadosSql = cursor.fetchall()
    textotese = cursor2.fetchall()
    
    #listas para tratar os dados iniciais
    usu = []
    posFinal = []
    dados = []
    tese = []
    
    #lista com dados após a remoção das stopwords
    sw_tese = []
    sw_posFinal = []
    aux_usu = []

    #lista com dados após a aplicação de Stemming
    st_posFinal = []
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
        posFinal.append(i[x+1].lower()) #lista com o posicionamento Final
        

#############################################################################################################
#Fases de pré-processamento linguistico
# - Remoção de stopwords
# - Troca de caracteres acentuados por caracteres não acentuados
# - Remoção pontuações
    for i in usu:
        aux_usu.append(removeStopWords(i))

    for i in tese:
        sw_tese.append(removeStopWords(i))


    for i in posFinal:
        sw_posFinal.append(removeStopWords(i))

#############################################################################################################
#Aplicação do RSPL Stemmer para remoção dos afixos das palavras da lingua portuguesa
#retirando afixos dos textos do posFinal e tese
    stemmer = RSLPStemmer()

    for i in range(len(sw_posFinal)):
        st_aux = sw_posFinal[i]
        string_aux = ""
        for sufixo in st_aux.split():
            string_aux = string_aux + " " + stemmer.stem(sufixo)
        
        st_posFinal.append(string_aux)

    for i in range(len(sw_tese)):
        st_aux = sw_tese[i]
        string_aux = ""
        for sufixo in st_aux.split():
            string_aux = string_aux + " " + stemmer.stem(sufixo)
        
        st_tese.append(string_aux)

#############################################################################################################
#TESTES!!!!!!!


#############################################################################################################
#retorno da função - usado na views.py para alimentar o template debate.html
#passar parametros que devem ser apresentados na templates debate.html
    return [st_tese, posFinal, sw_tese, aux_usu, st_posFinal]


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



    
