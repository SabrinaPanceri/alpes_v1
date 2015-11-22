# -*- coding: utf-8 -*-
 
from scipy.linalg import norm
import re, math
from collections import Counter
from unicodedata import normalize
from nltk.corpus import stopwords
from nltk import RegexpTokenizer
from nltk.stem import RSLPStemmer

palavras = RegexpTokenizer("[\w']+", flags=re.UNICODE)

def similaridadeCossenos(text1, text2):
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
    aux = texto.lower().replace(',',' ').replace('.',' ').replace('(','')
    aux = aux.replace(')','').replace('?','').replace('!','').replace('[','').replace(']','')
    aux = aux.replace('\r','').replace('\n','').replace('\t','')
    aux = aux.replace('=',' ').replace('"',' ').replace('{','').replace('}','')
    aux = aux.replace("'",' ').replace('`',' ')
    aux = aux.replace(':','').replace('/','').replace('http','')
    return aux

def removeNum(texto):
    aux = texto.lower().replace('1','').replace('2','').replace('3','').replace('4','')
    aux = aux.replace('5','').replace('6','').replace('7','').replace('8','').replace('9','')
    aux = aux.replace('0','')
    return aux

def removeA(texto):
    aux = normalize('NFKD', texto).encode('ASCII','ignore').decode('ASCII')
    return aux

def removeSE(texto):
    aux = texto.lower().replace('-se','')
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



#### REMOÇÃO DAS PALAVRAS CLASSIFICADAS
#### COMO ARTIGOS, PREPOSIÇÕES, ETC...
#### DEIXE NO CORPUS DE ANÁLISE APENAS OS TERMOS RELEVANTES:
#### ADJETIVOS, VERBOS AUXILIARES, SUBSTANTIVOS, VERBOS,
def limpaCorpus(texto):
    aux = []
    
    etiquetas = ["PDEN","N","V","ADJ","PCP","VAUX"]
                   
    for i in range(len(texto)):
        for j in range(len(texto[i])):
            if len(texto[i][j][0]) > 2 and texto[i][j][1] in etiquetas:
#                 print texto[i][j]
                aux.append(texto[i][j])
    
#     print "SEM STOPWORDS:", aux
    
    return aux


# def removeEndWeb(textoHttp):
#     auxHttp = re.sub(r'(?i)\b((?:http[s]?|www\d{0,3}|[a-z0-9.\-]|[a-z0-9.\-]+[a-z]{2,4}\/))', '', textoHttp)
#     return auxHttp

  
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

def stemming(texto):
#############################################################################################################
#Aplicação do RSPL Stemmer para remoção dos afixos das palavras da lingua portuguesa
#retirando afixos dos textos do posInicial e tese    

    stemmer = RSLPStemmer()
    st_texto = []
    
#     print texto

    for i in range(len(texto)):
        st_aux = texto[i]
        string_aux = ""
        for sufixo in st_aux:
            string_aux = string_aux + " " + stemmer.stem(sufixo)
        st_texto.append(string_aux)
    
#     print "stemming, st_texto", st_texto
    return st_texto



#############################################################################################################
