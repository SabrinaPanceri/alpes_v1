# -*- coding: utf-8 -*-
#encoding =utf8

import codecs
import re
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
### NUM1 = NUMERO DA LINHA DE REFERENCIA PARA VERBO SINONIMO
### NUM2 = NUMERO DA LINHA DE REFERENCIA PARA VERBO ANTONIMO (SENTIDO OPOSTO)
##############################################################################################################

def normalizacao(termo, etiqueta):
    
    
    sinonimo = []
    
    #abre o arquivo com as relacoes de sinonimia (termos sinonimos) e antonimia (termos contrarios) 
    base_tep = codecs.open('/home/panceri/git/alpes_v1/base_tep2/base_tep.txt', 'r', 'UTF8')
    
    #variavel com conteúdo do arquivo em memoria
    wordNet = base_tep.readlines()
    
    
    #fechar arquivo
    base_tep.close()
    
    #busca termo dentro de arquivo
    if etiqueta == "N":
        print "ANALISANDO SUBSTANTIVO"
        print termo, etiqueta
        for sinonimos in wordNet:
            if(sinonimos.find("[Substantivo]")>-1): 
                if(sinonimos.find(termo)>-1):            
                    print "termo", termo
                    print "sinonimos por linha", sinonimos
                    sinonimo.append(sinonimos)
    elif etiqueta == "ADJ":
        print "ANALISANDO ADJETIVOS"
        print termo, etiqueta
        for sinonimos in wordNet:
            if(sinonimos.find("[Adjetivo]")>-1): 
                if(sinonimos.find(termo)>-1):            
                    print "termo", termo
                    print "sinonimos por linha", sinonimos
                    sinonimo.append(sinonimos)
    elif etiqueta == "V" or etiqueta == "VAUX":
        print "ANALISANDO VERBOS"
        print termo, etiqueta
        for sinonimos in wordNet:
            if(sinonimos.find("[Verbo]")>-1): 
                if(sinonimos.find(termo)>-1):            
                    print "termo", termo
                    print "sinonimos por linha", sinonimos
                    sinonimo.append(sinonimos)
    else:
        print "ANALISANDO OUTROS -> NPROP, PCP, PDEN"
        print termo, etiqueta
        for sinonimos in wordNet: 
            if(sinonimos.find(termo)>-1):            
                print "termo", termo
                print "sinonimos por linha", sinonimos
                sinonimo.append(sinonimos)
    
   # print "todos os sinonimos", sinonimo 
    return sinonimo