# -*- coding: utf-8 -*-
#encoding =utf8

import codecs
import re

def organizaWordnet():

    base_tep = codecs.open('/home/panceri/git/alpes_v1/base_tep2/base_tep.txt', 'r', 'UTF8')
    wordnet = []
    #variavel com conteúdo do arquivo em memoria
    #não imprimir essa variável, MUITO GRANDEE!!!
    wordNet = base_tep.readlines()
    
    #fechar arquivo 
    base_tep.close()
    

### 263. [Verbo] {consentir, deixar, permitir} <973>
### 1ª linha do arquivo
### 1. [Verbo] {exagerar, exceder, quinta-essenciar, rebuscar, refinar, requintar} 
    
    x = 0
    for i in range(len(wordNet)):
        print i
        print "split", wordNet[i].split(" ")
        
#         print "termos",re.findall('{[^}]*}', i)
#         
#         print "num",re.findall('[[0-9]^.]*.', i)
        exit()
    
    
    
    
    
#     for sinonimos in wordNet:
#         print re.findall('{[^}]*}', sinonimos)
#         exit()
  
    
    
    return True

