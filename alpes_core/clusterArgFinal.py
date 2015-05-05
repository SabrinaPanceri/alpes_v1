# -*- coding: utf-8 -*-

import HTMLParser
import re
from django.db import connection
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from nltk.cluster.util import cosine_distance
from alpes_core.similarity import removeStopWords
from nltk.stem import RSLPStemmer

def clusterArgFinal(idtese):
    vectorizer = CountVectorizer()
    h = HTMLParser.HTMLParser()

    cursor = connection.cursor()
    cursor2 = connection.cursor()

    cursor.execute("select distinct `usr`.`primeironome` as `name`, `pos`.`posicionamentofinal` AS `posicionamentofinal` from ((((`argumento` `arg` join `revisao` `rev`) join `replica` `rep`) join `posicionamento` `pos`) join `argumentador` `urg`)join `usuario` `usr`  where ((`arg`.`tese_idtese` = " + idtese + "  ) and (`rev`.`argumento_idargumento` = `arg`.`idargumento`) and (`rep`.`revisao_idrevisao` = `rev`.`idrevisao`) and (`arg`.`argumentador_idargumentador` = `pos`.`argumentador_idargumentador`) and (`arg`.`tese_idtese` = `pos`.`tese_idtese`) and (`arg`.`posicionamentoinicial` is not null) and (`arg`.`argumentador_idargumentador` = `urg`.`idargumentador`) and(`urg`.`usuario_idusuario` = `usr`.`idusuario`) and (`pos`.`posicionamentofinal` is not null))")
    cursor2.execute("select tese from tese where grupo_idgrupo = 1064 ")

    dadosSql = cursor.fetchall()
    textotese = cursor2.fetchall()

    usu = []
    posFinal = []

    dados = []
    tese = []

    sw_tese = []
    sw_posFinal = []
    aux_usu = []

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

    #Aplicação do RSPL Stemmer para remoção dos afixos das palavras da lingua portuguesa
    #retirando afixos dos textos do posFinal e tese
    stemmer = RSLPStemmer()

    st_posFinal = []
    st_tese = []

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

    return [st_tese, sw_posFinal, sw_tese, aux_usu, st_posFinal]


