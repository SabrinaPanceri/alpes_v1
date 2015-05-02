# -*- coding: utf-8 -*-
 

import re, math
from collections import Counter
from unicodedata import normalize
from nltk.corpus import stopwords
from nltk import RegexpTokenizer, bigrams, trigrams

palavras = RegexpTokenizer("[\w']+", flags=re.UNICODE)

def similaridade(text1, text2):
    intersecao = set(text1.keys()) & set(text2.keys())
    numerador = sum([text1[x] * text2[x] for x in intersecao])

    soma1 = sum([text1[x]**2 for x in text1.keys()])
    soma2 = sum([text2[x]**2 for x in text2.keys()])
    denominador = math.sqrt(soma1) * math.sqrt(soma2)

    if not denominador:
        return 0.0
    else:
        return float(numerador) / denominador

# palavras = re.compile(r'\w+')

def removeA(texto):
    aux = normalize('NFKD', texto).encode('ASCII','ignore').decode('ASCII')
    return aux

def removeStopWords(texto):
    aux = ""
    # função da NLTK que retorna as stopwords na lingua portuguesa
    stop = stopwords.words('portuguese')
    stopP = []
    for s in stop:
        stopP.append(removeA(s))
#     print stopP

    #remove acentuação
    textoaux = removeA(texto)

    # divide o texto em palavras    
#     words = palavras.findall(textoaux)
    words = palavras.tokenize(textoaux)
#     print words
    
    #retira pontuações do texto e divide o texto em palavras
    for i in words:
        #retira as stopwords da lingua portuguesa do texto do artigo que está sendo apresentado
        if i not in stopP:
            #ignora palavras com menos de 3 caracteres
            if len(i) > 2:
                aux = aux + " " + i
    return aux

                
def vetores(texto):
#     words = palavras.findall(texto)
    words = palavras.tokenize(texto)
    print words
    return Counter(words)