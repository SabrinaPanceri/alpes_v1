#coding: utf-8

from django.db import models
from django.db import connections, connection
import re


# from django.contrib.auth.models import User
# from django.db.models.signals import post_save

#Import's necessarios
from nltk.corpus import stopwords
from nltk import FreqDist
# from alpes_core.similarity import similarity, vetores

class Tese(models.Model):
    idtese = models.AutoField(primary_key=True)
    grupo_idgrupo = models.TextField()
    tese = models.TextField()
    
    class Meta:
        db_table = 'tese'

class Argumentador(models.Model):
    idargumentador = models.AutoField(primary_key=True)

    class Meta:
        db_table = 'argumentador'

class Posicionamento(models.Model):
    argumentador_idargumentador = models.IntegerField(primary_key=True)
    tese_idtese = models.IntegerField(primary_key=True)
    posicionamentofinal = models.TextField()

    class Meta:
        db_table = 'posicionamento'
      
class Argumento(models.Model):
    idargumento = models.AutoField(primary_key=True)
    posicionamentoinicial = models.TextField()
    argumento = models.TextField()
    
    class Meta:
        db_table = 'argumento'
        
class Revisao(models.Model):
    idrevisao = models.AutoField(primary_key = True)
    revisao = models.TextField()
    
    class Meta:
        db_table = 'revisao'
        
class Replica(models.Model):
    revisao_idrevisao = models.IntegerField(primary_key=True)
    argumentador_idargumentador = models.IntegerField(primary_key=True)
    replica = models.TextField()
    
    class Meta:
        db_table = 'replica'


# #Execução do SQL
# cursor = connection.cursor()
#  
# idtese = "1472"
#  
# cursor.execute("select `arg`.`posicionamentoinicial` AS `posicionamentoinicial`, `arg`.`argumento` AS `argumento`, `rev`.`revisao` AS `revisao`, `rep`.`replica` AS `replica`, `pos`.`posicionamentofinal` AS `posicionamentofinal` from (((`argumento` `arg` join `revisao` `rev`) join `replica` `rep`) join `posicionamento` `pos`) where ((`arg`.`tese_idtese` = " + idtese + " ) and (`rev`.`argumento_idargumento` = `arg`.`idargumento`) and (`rep`.`revisao_idrevisao` = `rev`.`idrevisao`) and (`arg`.`argumentador_idargumentador` = `pos`.`argumentador_idargumentador`) and (`arg`.`tese_idtese` = `pos`.`tese_idtese`) and (`arg`.`posicionamentoinicial` is not null) and (`arg`.`argumento` is not null) and (`rev`.`revisao` is not null) and (`rep`.`replica` is not null) and (`pos`.`posicionamentofinal` is not null))")
# dados = cursor.fetchall()
# 
# arg = []
# pI = []
# rev = []
# rep = []
# posFinal = []
# 
# for i in dados:
#     x = 0
#     arg.append(i[x])
#     pI.append(i[x+1])
#     rev.append(i[x+2])
#     rep.append(i[x+3])
#     posFinal.append(i[x+4])
#     x = x + 1
    
# 
# 
# def getTitulosSemelhantes(self):
#         artigosSim = []
#         
#         titulo1 = self.dados.lower()
#         
#         aux1 = vetores(titulo1)
# 
#         for  i in range(0,len(dados)):            
#             titulo2 = dados[i].titulo_artigo.lower()
#             aux2 = vetores(titulo2)
#             
#             if self.id != dados[i].id and similarity(aux1, aux2):
#                 artigosSim.append(dados[i])
#                 
#         return artigosSim
# 
# def palavrasChaves(self):
#         # função da NLTK que retorna as stopwords na lingua inglesa
#         stopE = stopwords.words('english')
# 
#         # função da NLTK que retorna as stopwords na lingua portuguesa
#         stop = stopwords.words('portuguese')  
#               
#         stopS = stopwords.words('spanish')
#         
#         palavrasChaves = [] 
#         textoArtigo = []
#         
#         #retira pontuações do texto e divide o texto em palavras
#         for i in self.texto_artigo.lower().replace(',','').replace('.','').replace('-','').replace('(','').replace(')','').split():
#             #retira as stopwords da lingua portuguesa do texto do artigo que está sendo apresentado
#             if i not in stop:
#                 #retira as stopwords da lingua inglesa do texto do artigo que está sendo apresentado
#                 if i not in stopE:
#                     #ignora palavras com menos de 3 caracteres. Isso é para tratar palavras, como por exemplo o verbo "É"
#                     if i not in stopS:
#                             if len(i) > 2:
#                                 textoArtigo.append(i)
#         
#         # apresenta a frequencia de repeticoes das palavras no corpo do artigo
#         freq = FreqDist(textoArtigo)
#         
#         # separa as quatro palavras mais frequentes
#         items = freq.items()[:4]
#         
#         # coloca as palavras mais frequentes do texto na variavel palavrasChaves
#         for i in range(0,len(items)):
#             palavrasChaves.append(items[i][0].upper())
#             
#         return palavrasChaves       



 







