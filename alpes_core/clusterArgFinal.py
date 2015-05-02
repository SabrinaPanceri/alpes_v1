# -*- coding: utf-8 -*-

from sklearn.feature_extraction.text import CountVectorizer
from django.db import connection
import HTMLParser
import re

from alpes_core.similarity import similaridade, vetores, asciize

vectorizer = CountVectorizer()
h = HTMLParser.HTMLParser()
h1 = HTMLParser.HTMLParser()

cursor = connection.cursor()
cursor2 = connection.cursor()
 
idtese = "1472"

cursor.execute("select distinct `usr`.`primeironome` as `name`, `pos`.`posicionamentofinal` AS `posicionamentofinal` from ((((`argumento` `arg` join `revisao` `rev`) join `replica` `rep`) join `posicionamento` `pos`) join `argumentador` `urg`)join `usuario` `usr`  where ((`arg`.`tese_idtese` = " + idtese + "  ) and (`rev`.`argumento_idargumento` = `arg`.`idargumento`) and (`rep`.`revisao_idrevisao` = `rev`.`idrevisao`) and (`arg`.`argumentador_idargumentador` = `pos`.`argumentador_idargumentador`) and (`arg`.`tese_idtese` = `pos`.`tese_idtese`) and (`arg`.`posicionamentoinicial` is not null) and (`arg`.`argumentador_idargumentador` = `urg`.`idargumentador`) and(`urg`.`usuario_idusuario` = `usr`.`idusuario`) and (`pos`.`posicionamentofinal` is not null))")
cursor2.execute("select tese from tese where grupo_idgrupo = 1064 ")

dadosSql = cursor.fetchall()
textotese = cursor2.fetchall()

usu = []
posFinal = []

dados = []
aux_tese = []

similares = []

#Aplicacao de Case Folding
for d in dadosSql:
    dados.append([re.sub('<[^>]*>', '', h.unescape(d[0])).lower(),
                  re.sub('<[^>]*>', '', h.unescape(d[1])).lower()])

for t in textotese:
    aux_tese.append(re.sub('<[^>]*>', '', h.unescape(t[0])).lower())

#Colocando os textos de posicionamento final em numa lista separada
for i in dados:
    x = 0
    usu.append(i[x])
    posFinal.append(i[x+1].lower()) #lista com o posicionamento Final


aux1 = asciize(aux_tese[0])

aux1 = vetores(aux_tese[0])

# for i in range(len(posFinal)):
    


