#coding: utf-8

from django.db import models
# from django.contrib.auth.models import User
# from django.db.models.signals import post_save

#Import's necessarios
# from nltk.corpus import stopwords
# from nltk import FreqDist
from alpes_core.similarity import similarity, vetores



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

