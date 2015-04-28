#coding: utf-8

from django.db import models
# from django.contrib.auth.models import User
# from django.db.models.signals import post_save

#Import's necessarios
# from nltk.corpus import stopwords
# from nltk import FreqDist
from alpes_core.similarity import similarity, vetores

# Create your models here.
class Posicionamento(models.Model):
    argumentacaoFinal = models.TextField()

        
    class Meta:
        db_table = 'posicionamento'
    
    def grupoArgumentacao(self):
        posFinal = Posicionamento.objects.all()
#         print posFinal
        
        similares = []
        
        titulo1 = self.argumentacaoFinal.lower()
        
        aux1 = vetores(titulo1)

        for  i in range(0,len(posFinal)):            
            titulo2 = posFinal[i].argumentacaoFinal.lower()
            aux2 = vetores(titulo2)
            
            if self.id != posFinal[i].id and similarity(aux1, aux2):
                similares.append(posFinal[i])
                
        return similares
    
#     def palavrasChaves(self):
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