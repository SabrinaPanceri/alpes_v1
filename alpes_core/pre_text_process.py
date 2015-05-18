# -*- coding: utf-8 -*-
 
from scipy.linalg import norm
import re, math
from collections import Counter
from unicodedata import normalize
from nltk.corpus import stopwords
from nltk import RegexpTokenizer

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


def removePontuacao(texto):
    aux = texto.lower().replace(',',' ').replace('.',' ').replace('-',' ').replace('(',' ').replace(')',' ').replace('?',' ').replace('!',' ').replace('[',' ').replace(']',' ').replace(':',' ').replace('/',' ').replace('\r',' ').replace('\n',' ').replace('\t',' ').replace('=',' ').replace('"',' ')
    return aux

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
    textoaux = removeA(removePontuacao(texto))

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


def simple_cosine_sim(a, b):
    if len(b) < len(a):
        a, b = b, a

    res = 0
    for key, a_value in a.iteritems():
        res += a_value * b.get(key, 0)
    if res == 0:
        return 0

    try:
        res = res / norm(a.values()) / norm(b.values())
    except ZeroDivisionError:
        res = 0
    return res 