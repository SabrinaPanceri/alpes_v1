#coding: utf-8
from django.db import models

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
