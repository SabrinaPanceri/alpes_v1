# -*- coding: utf-8 -*-
# Algoritmo de Cosine adaptado 

import re, math
from collections import Counter
from unicodedata import normalize

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

def removeA(texto):
    aux = normalize('NFKD', texto).encode('ASCII','ignore').decode('ASCII')
    return aux

palavras = re.compile(r'\w+')

def vetores(text):
    textoAux = removeA(text)
    words = palavras.findall(textoAux)
    print words
    return Counter(words)
