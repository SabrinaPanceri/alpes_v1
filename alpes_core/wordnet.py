# -*- coding: utf-8 -*-

import codecs

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

def normalizacao(termo):
    sinonimo = ""
    
    #abre o arquivo com as relacoes de sinonimia (termos sinonimos) e antonimia (termos contrarios) 
    base_tep2 = open('/home/panceri/git/alpes_v1/base_tep2/base_tep2.txt', 'r')
    
    #variavel com conteúdo do arquivo em memoria
    arquivo = base_tep2.readlines() 
    
    #fechar arquivo
    base_tep2.close()
    
    #busca termo dentro de arquivo
    for f in arquivo:
        if(f.find(termo)>-1):
            print f
    
    
    
    
    
    
    
    
    
    return sinonimo