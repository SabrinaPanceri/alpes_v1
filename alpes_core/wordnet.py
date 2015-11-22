# -*- coding: utf-8 -*-
#encoding =utf8

import codecs
import re
from alpes_core.textProcess import removeA, removePontuacao, stemming
from pprint import pprint
from nltk import RSLPStemmer


##############################################################################################################
### A NORMALIZACAO DE TERMOS REFERE-SE A TECNICA DE TROCAR PALAVRAS SINONIMAS, OU SEJA, QUE TENHAM SIGNIFICADO
### SEMELHANTE, POR UM UNICO TERMO REPRESENTATIVO NO CORPUS DE ANALISE. DESSA FORMA, É POSSIVEL AUMENTAR O GRAU
### DE SIMILARIDADE ENTRE OS TEXTOS ANALISADOS ATRAVES DO USO DE TECNICAS DE ANALISE ESTATISTICAS, COMO SIMILA
### RIDADE DE COSSENOS OU DISTANCIA EUCLIDIANA.
###
### A NORMALIZACAO FOI DESENVOLVIDA COM BASE NOS DADOS DISPONIBILIZADOS PELO PROJETO TEP 2.0 DO NILC/USP
### http://143.107.183.175:21480/tep2/index.htm
### 
### FORMATO DO ARQUIVO
### NUM1. [Tipo] {termos sinonimos} <NUM2>
### 263. [Verbo] {consentir, deixar, permitir} <973>
### NUM1 = NUMERO DA LINHA DE REFERENCIA PARA TERMO SINONIMO
### NUM2 = NUMERO DA LINHA DE REFERENCIA PARA TERMO ANTONIMO (SENTIDO OPOSTO)
##############################################################################################################

def normalizacao(dicSin, termo, etiqueta):
    #variáveis locais
    sinonimo = []
    SA_wordnet = []
    aux = []
    
    #abre o arquivo com as relacoes de sinonimia (termos sinonimos) e antonimia (termos contrarios) 
    base_tep = codecs.open('/home/panceri/git/alpes_v1/base_tep2/base_tep.txt', 'r', 'UTF8')
    
    #variavel com conteúdo do arquivo em memoria
    #não imprimir essa variável, MUITO GRANDEE!!!
    wordNet = base_tep.readlines()
    
    #fechar arquivo 
    base_tep.close()
    
    #retirar acentos da base
    for i in wordNet:
        SA_wordnet.append(removeA(i))
    
    #teste com busca pelo radical (stemmer)
    radicais = RSLPStemmer()
    
#     termoStm = radicais.stem(termo)

    # busca termo dentro de arquivo
    # armazena termo como chave do dicionario
    # os sinonimos são armazenados como uma lista
    if etiqueta == "N":
        for sinonimos in SA_wordnet:
            if(sinonimos.find("[Substantivo]")>=0):
                if(sinonimos.find(termo)>=0):
                    aux1 = re.findall('{[^}]*}', sinonimos)
                    for a in aux1:
                        aux2 = re.findall('^[0-9]*.', sinonimos) #retorna o numero de referencia dos sinonimos
                        auxN = removePontuacao(a) #lista de sinonimos sem as {}
                        for b in auxN.split():
                            x = radicais.stem(b)
                            if termo == x:
                                aux.append(aux2)
        dicSin[termo] = aux
    elif etiqueta == "ADJ":
        for sinonimos in wordNet:
            if(sinonimos.find("[Adjetivo]")>=0):
                if(sinonimos.find(termo)>=0):
                    aux1 = re.findall('{[^}]*}', sinonimos)
                    for a in aux1:
                        aux2 = re.findall('^[0-9]*.', sinonimos) #retorna o numero de referencia dos sinonimos
                        auxAD = removePontuacao(a) #lista de sinonimos sem as {}
                        for b in auxAD.split():
                            x = radicais.stem(b)
                            if termo == x:
                                aux.append(aux2)
        dicSin[termo] = aux
         
    elif etiqueta == "V" or etiqueta == "VAUX":
        for sinonimos in wordNet:
            if(sinonimos.find("[Verbo]")>=0):
                if(sinonimos.find(termo)>=0):            
                    aux1 = re.findall('{[^}]*}', sinonimos)
                    for a in aux1:
                        aux2 = re.findall('^[0-9]*.', sinonimos) #retorna o numero de referencia dos sinonimos
                        auxV = removePontuacao(a)
                        for b in auxV.split():
                            x = radicais.stem(b)
                            if termo == x:
                                aux.append(aux2)
        dicSin[termo] = aux
    else: #PARA TRATAR OS ADVÉRBIOS
        for sinonimos in wordNet: 
            if(sinonimos.find(termo)>=0):
                aux1 = re.findall('{[^}]*}', sinonimos)
                for a in aux1:
                    aux2 = re.findall('^[0-9]*.', sinonimos) #retorna o numero de referencia dos sinonimos
                    auxO = removePontuacao(a)
#                     termoStmO = radicais.stem(termo) #radical de formação do termo de busca (stem)
                    for b in auxO.split():
                        x = radicais.stem(b)
                        if termo == x:
                            aux.append(aux2)
        dicSin[termo] = aux
    
    return sinonimo