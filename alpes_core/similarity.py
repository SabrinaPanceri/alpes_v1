# -*- coding: utf-8 -*-
# Algoritmo de Cosine adaptado 

import re, math
from collections import Counter

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

_table = { 
    "á" : "a", "à" : "a", "â" : "a", "ä" : "a", "ã" : "a", "å" : "a",
    "é" : "e", "è" : "e", "ê" : "e", "ë" : "e",
    "í" : "i", "ì" : "i", "î" : "i", "ï" : "i",
    "ó" : "o", "ò" : "o", "ô" : "o", "ö" : "o", "õ" : "o", "ø" : "o", 
    "ú" : "u", "ù" : "u", "û" : "u", "ü" : "u",
    "ñ" : "n", "ç" : "c",
    "Á" : "A", "À" : "A", "Â" : "A", "Ä" : "A", "Ã" : "A", "Å" : "A",
    "É" : "E", "È" : "E", "Ê" : "E", "Ë" : "E", 
    "Í" : "I", "Ì" : "I", "Î" : "I", "Ï" : "I", 
    "Ó" : "O", "Ò" : "O", "Ô" : "O", "Ö" : "O", "Õ" : "O", "Ø" : "O",
    "Ú" : "U", "Ù" : "U", "Û" : "U", "Ü" : "U", 
    "Ñ" : "N", "Ç" : "C",
    "ß" : "ss", "Þ" : "d" , "æ" : "ae"
}


def asciize(s):
    """ 
    Converts a entire string to a ASCII only string.
   
    string
        The string to be converted.
    """
    for original, plain in _table.items():
        print original
        print plain
        print s
        s = s.replace(original, plain)
        
    return s


palavras = re.compile(r'\w+')

def vetores(text):
#     aux = retiraAcentos(text)
    words = palavras.findall(text)
    print words
    return Counter(words)
