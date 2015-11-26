# -*- coding: utf-8 -*-
#encoding =utf8

import codecs
import re
from alpes_core.textProcess import removeA, removePontuacao
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

def normalizacao(dicSin, termo, radical, etiqueta):
    #variáveis locais
    SA_wordnet = [] #armazena a wordnet sem acentos   
    listaTodosSin = [] #lista com todos os termos sinonimos encontrados
    listaNumRef = [] #lista com o número da linha de referência dos termos sinominos 
    
    #abre o arquivo com as relacoes de sinonimia (termos linhaWordNet) e antonimia (termos contrarios) 
    base_tep = codecs.open('/home/panceri/git/alpes_v1/base_tep2/base_tep.txt', 'r', 'UTF8')
    dicionario = open('/home/panceri/git/alpes_v1/base_tep2/dicionarioSinonimos.txt', 'w')
    
    #variavel com conteúdo do arquivo em memoria
    #não imprimir essa variável, MUITO GRANDEE!!!
    wordNet = base_tep.readlines()
    
    #fechar arquivo 
    base_tep.close()
    
    #retirar acentos da base
    for i in wordNet:
        SA_wordnet.append(removeA(i))
    
    #teste com busca pelo radical (stemmer)
    stemmer = RSLPStemmer()
    
#     termoStm = stemmer.stem(termo)

    
#     print termo, radical, etiqueta

    # busca termo dentro de arquivo
    # armazena termo como chave do dicionario
    # os linhaWordNet são armazenados como uma lista
    if etiqueta == "N":
        for linhaWordNet in SA_wordnet:
            if(linhaWordNet.find("[Substantivo]")>=0):
                if(linhaWordNet.find(termo)>=0):
                    listaSinonimos = re.findall('{[^}]*}', linhaWordNet)
                    for palavraSinonima in listaSinonimos:
                        numRefSin = re.findall('^[0-9]*.', linhaWordNet) #retorna o numero de referencia dos linhaWordNet
                        sa_palavraSinonima = removePontuacao(palavraSinonima) #lista de linhaWordNet sem as {}
                        for termSinWordNet in sa_palavraSinonima.split():
                            st_termSinWordNet = stemmer.stem(termSinWordNet)
                            if radical == st_termSinWordNet:
                                listaNumRef.append(numRefSin)
                            listaTodosSin.append(termSinWordNet)
        dicSin[termo] = listaNumRef,listaTodosSin

    elif etiqueta == "ADJ":
        for linhaWordNet in wordNet:
            if(linhaWordNet.find("[Adjetivo]")>=0):
                if(linhaWordNet.find(termo)>=0):
                    listaSinonimos = re.findall('{[^}]*}', linhaWordNet)
                    for palavraSinonima in listaSinonimos:
                        numRefSin = re.findall('^[0-9]*.', linhaWordNet) #retorna o numero de referencia dos linhaWordNet
                        sa_palavraSinonima = removePontuacao(palavraSinonima) #lista de linhaWordNet sem as {}
                        for termSinWordNet in sa_palavraSinonima.split():
                            st_termSinWordNet = stemmer.stem(termSinWordNet)
                            if radical == st_termSinWordNet:
                                listaNumRef.append(numRefSin)
                            listaTodosSin.append(sa_palavraSinonima)
        dicSin[termo] = listaNumRef,listaTodosSin

    elif etiqueta == "V" or etiqueta == "VAUX":
        for linhaWordNet in wordNet:
            if(linhaWordNet.find("[Verbo]")>=0):
                if(linhaWordNet.find(termo)>=0):            
                    listaSinonimos = re.findall('{[^}]*}', linhaWordNet)
                    for palavraSinonima in listaSinonimos:
                        numRefSin = re.findall('^[0-9]*.', linhaWordNet) #retorna o numero de referencia dos linhaWordNet
                        sa_palavraSinonima = removePontuacao(palavraSinonima)
                        for termSinWordNet in sa_palavraSinonima.split():
                            st_termSinWordNet = stemmer.stem(termSinWordNet)
                            if radical == st_termSinWordNet:
                                listaNumRef.append(numRefSin)
                                listaTodosSin.append(sa_palavraSinonima)
        dicSin[termo] = listaNumRef
    else: #PARA TRATAR OS ADVÉRBIOS
        for linhaWordNet in wordNet: 
            if(linhaWordNet.find(termo)>=0):
                listaSinonimos = re.findall('{[^}]*}', linhaWordNet)
                for palavraSinonima in listaSinonimos:
                    numRefSin = re.findall('^[0-9]*.', linhaWordNet) #retorna o numero de referencia dos linhaWordNet
                    sa_palavraSinonima = removePontuacao(palavraSinonima)
                    for termSinWordNet in sa_palavraSinonima.split():
                        st_termSinWordNet = stemmer.stem(termSinWordNet)
                        if radical == st_termSinWordNet:
                            listaNumRef.append(numRefSin)
                            listaTodosSin.append(sa_palavraSinonima)
        dicSin[termo] = listaNumRef
    
    
### verificar como imprimir isso num arquivo
### veriricar como imprimir um dicionario num arquivo txt    
    listaux = []
    for termo, listaNumRef in dicSin.items():
        temp = '{}: {}'.format(termo, listaNumRef)
#         print '{}: {}'.format(termo, listaNumRef)
        listaux.append(temp)
        
        dicionario.write(temp)
    
    dicionario.close()
#     exit()
    
