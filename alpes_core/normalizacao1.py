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

def normalizacaoWordnet(dicSin, termo, radical, etiqueta):
    #variáveis locais
    SA_wordnet = [] #armazena a wordnet sem acentos   
    listaTodosSin = [] #lista com todos os termos sinonimos encontrados
    listaNumRef = [] #lista com o número da linha de referência dos termos sinominos
    listaDicion = [] 
    
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
        for linhaWordNet in wordNet:
            if(linhaWordNet.find("[Substantivo]")>=0):
                termosSinonimos = re.findall('{[^}]*}', linhaWordNet)
                for listaSinonimos in termosSinonimos:
                    sa_listaSinonimos = removePontuacao(listaSinonimos) #lista de linhaWordNet sem as {}
                    for palavraSinonima in sa_listaSinonimos.split():
                        st_palavraSinonima = stemmer.stem(palavraSinonima)
                        auxTermos = sa_listaSinonimos.split()
                        if radical == st_palavraSinonima:
                            numETerm =  re.findall('^[0-9]*.+{[^}]*}', linhaWordNet)
                            listaDicion.append(numETerm)
        dicSin[termo] = listaDicion

    elif etiqueta == "ADJ":
        for linhaWordNet in wordNet:
            if(linhaWordNet.find("[Adjetivo]")>=0):
                termosSinonimos = re.findall('{[^}]*}', linhaWordNet)
                for listaSinonimos in termosSinonimos:
                    sa_listaSinonimos = removePontuacao(listaSinonimos) #lista de linhaWordNet sem as {}
                    for palavraSinonima in sa_listaSinonimos.split():
                        st_palavraSinonima = stemmer.stem(palavraSinonima)
                        auxTermos = sa_listaSinonimos.split()
                        if radical == st_palavraSinonima:
                            numETerm =  re.findall('^[0-9]*.+{[^}]*}', linhaWordNet)
                            listaDicion.append(numETerm)
        dicSin[termo] = listaDicion


    elif etiqueta == "V" or etiqueta == "VAUX":
        for linhaWordNet in wordNet:
            if(linhaWordNet.find("[Verbo]")>=0):
                termosSinonimos = re.findall('{[^}]*}', linhaWordNet)
                for listaSinonimos in termosSinonimos:
                    sa_listaSinonimos = removePontuacao(listaSinonimos) #lista de linhaWordNet sem as {}
                    for palavraSinonima in sa_listaSinonimos.split():
                        st_palavraSinonima = stemmer.stem(palavraSinonima)
                        auxTermos = sa_listaSinonimos.split()
                        if radical == st_palavraSinonima:
                            numETerm =  re.findall('^[0-9]*.+{[^}]*}', linhaWordNet)
                            listaDicion.append(numETerm)
        dicSin[termo] = listaDicion

    else: #PARA TRATAR OS ADVÉRBIOS
        for linhaWordNet in wordNet: 
            termosSinonimos = re.findall('{[^}]*}', linhaWordNet)
            for listaSinonimos in termosSinonimos:
                sa_listaSinonimos = removePontuacao(listaSinonimos) #lista de linhaWordNet sem as {}
                for palavraSinonima in sa_listaSinonimos.split():
                    st_palavraSinonima = stemmer.stem(palavraSinonima)
                    auxTermos = sa_listaSinonimos.split()
                    if radical == st_palavraSinonima:
                            numETerm =  re.findall('^[0-9]*.+{[^}]*}', linhaWordNet)
                            listaDicion.append(numETerm)
        dicSin[termo] = listaDicion
        pprint(dicSin)
        exit()

    
### verificar como imprimir isso num arquivo
### veriricar como imprimir um dicionario num arquivo txt    
#     listaux = []
#     for termo, listaNumRef in dicSin.items():
#         temp = '{}: {}'.format(termo, listaNumRef)
# #         print '{}: {}'.format(termo, listaNumRef)
#         listaux.append(temp)
#         
#         dicionario.write(temp)
#     
#     dicionario.close()
#     exit()
    

