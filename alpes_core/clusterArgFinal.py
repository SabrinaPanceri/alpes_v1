# -*- coding: utf-8 -*-

from sklearn.feature_extraction.text import CountVectorizer
from django.db import connection
import HTMLParser
import re

from alpes_core.similarity import similaridade, vetores, removeStopWords

vectorizer = CountVectorizer()
h = HTMLParser.HTMLParser()

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

sw_aux_tese = []
sw_posFinal = []
aux_usu = []

grupo1 = []
grupo2 = []
grupo3 = []
grupo4 = []

#Aplicacao de Case Folding
for d in dadosSql:
    dados.append([re.sub('<[^>]*>', '', h.unescape(d[0])).lower(),
                  re.sub('<[^>]*>', '', h.unescape(d[1])).lower()])

for t in textotese:
    aux_tese.append(re.sub('<[^>]*>', '', h.unescape(t[0])).lower())
        

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

for i in aux_tese:
    sw_aux_tese.append(removeStopWords(i))


for i in posFinal:
    sw_posFinal.append(removeStopWords(i))

# vetores() -> Retorna a quantidade de palavras por posição

# aux = ""
# for i in sw_aux_tese:
#     aux = vetores(i)
#     
# for i in range(0, len(sw_posFinal)):
#     print "i", i
#     for j in range(i+1, len(sw_posFinal)):
#         print "j", j
#         aux1 = vetores(sw_posFinal[i])
#         aux2 = vetores(sw_posFinal[j])
#  
#         if j < len(sw_posFinal):
#             print similaridade(aux1, aux2)
#                        
#             if (similaridade(aux1, aux2)) >= 0 and (similaridade(aux1, aux2)) <= 0.4: 
#                 grupo1.append(aux_usu[i])
#             elif (similaridade(aux1, aux2)) > 0.4 and (similaridade(aux1, aux2)) <= 0.7:
#                 grupo2.append(aux_usu[i])
#             elif (similaridade(aux1, aux2)) > 0.7 and (similaridade(aux1, aux2)) <= 1:
#                 grupo3.append(aux_usu[i])
#             else: 
#                 grupo4.append(aux_usu[i])
                
    


