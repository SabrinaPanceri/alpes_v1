# -*- coding: utf-8 -*-
#encoding =utf8
##################################################################
### CÓDIGO DESENVOLVIDO POR SABRINA SIQUEIRA PANCERI            ##
### PROTÓTIPO DE SUA  DISSERTAÇÃO DE MESTRADO                   ##
### ESSE CÓDIGO PODE SER COPIADO, ALTERADO E DISTRIBUÍDO        ##
### DESDE QUE SUA FONTE SEJA REFERENCIADA                       ##
### PARA MAIS INFORMAÇÕES, ENTRE EM CONTATO ATRAVÉS DO EMAIL    ##
### SABRINASPANCERI@GMAIL.COM                                   ##
##################################################################

####################################################################################################################################
### A NORMALIZACAO DE TERMOS REFERE-SE A TECNICA DE TROCAR PALAVRAS SINONIMAS, OU SEJA, QUE TENHAM SIGNIFICADO                    ##
### SEMELHANTE, POR UM UNICO TERMO REPRESENTATIVO NO CORPUS DE ANALISE. DESSA FORMA, É POSSIVEL AUMENTAR O GRAU                   ##
### DE SIMILARIDADE ENTRE OS TEXTOS ANALISADOS ATRAVES DO USO DE TECNICAS DE ANALISE ESTATISTICAS, COMO SIMILA                    ##
### RIDADE DE COSSENOS OU DISTANCIA EUCLIDIANA.                                                                                   ##
###                                                                                                                               ##
### A NORMALIZACAO FOI DESENVOLVIDA COM BASE NOS DADOS DISPONIBILIZADOS PELO PROJETO TEP 2.0 DO NILC/USP                          ##
### http://143.107.183.175:21480/tep2/index.htm                                                                                   ##
###                                                                                                                               ## 
### FORMATO DO ARQUIVO                                                                                                            ##
### NUM1. [Tipo] {termos sinonimos} <NUM2>                                                                                        ##
### 263. [Verbo] {consentir, deixar, permitir} <973>                                                                              ##
### NUM1 = NUMERO DA LINHA DE REFERENCIA PARA TERMO SINONIMO                                                                      ##
### NUM2 = NUMERO DA LINHA DE REFERENCIA PARA TERMO ANTONIMO (SENTIDO OPOSTO)                                                     ##
####################################################################################################################################
### A ANÁLISE É REALIZADA COM BASE NO TEXTO SEM A EXCLUSÃO DOS ACENTOS                                                            ##
### POIS AO EXCLUÍ-LOS A REDUÇÃO AO RADICAL DE FORMAÇÃO (APLICAÇÃO DO RSLP) É PREJUDICADA                                         ##
### OS TESTES REALIZADOS MOSTRARAM QUE ESSA É UMA MELHOR ABORDAGEM, UMA VEZ QUE NOSSOS TEXTOS SÃO PEQUENOS                        ##
### E PRECISAMOS CHEGAR O MAIS PRÓXIMO POSSÍVEL SEM CONSIDERAR SEUS SENTIDOS E/OU CONTEXTOS                                       ##
####################################################################################################################################


from pprint import pprint

import yappi
import time

##########################################################################
### CRIAÇÃO DO DICIONÁRIO COM AS RELAÇÕES DE SINONÍMIA ENCONTRADAS     ###
### ALTERA A VARIÁVEL dicSin, RELACIONANDO O termo COM A LINHA AONDE   ###
### ESTÃO OS SEUS SINÔNIMOS.                                           ###
### A BUSCA É FEITA COM BASE NO STEMMER DO TERMO                       ###
### EXEMPLO DOS DADOS DO dicSin                                        ###
### u'velocidade': [[u'18751. [Substantivo] {apressuramento,           ###
### celeridade, ligeireza, pressa, rapidez, velocidade}']]}            ###
##########################################################################


def normalizacaoWordnet(st_WordNet, sw_tagcomAce_posInicial, st_tagcomAce_posInicial):
    
    norm_posInicial = []
    dicSin = {}
    
    qtdeTermosTotal = 0
    yappi.set_clock_type('cpu')
    yappi.start(builtins=True)      
    start = time.time() 
    
#########################################################################################
### BUSCA PELOS TERMOS SINÔNIMOS EM st_WordNet E MONTA O DICIONÁRIO COM AS RELAÇÕES    ##
#########################################################################################    

    for i in range(len(st_tagcomAce_posInicial)):
        qtdeTermos = 0
#         print datetime.now()
        for j in range(len(st_tagcomAce_posInicial[i])):
            termo = sw_tagcomAce_posInicial[i][j][0] #termo original digitado pelo aluno
            radical = st_tagcomAce_posInicial[i][j][0] #termo reduzido ao seu radical de formação (aplicação de stemmer - RSLP)
            etiqueta = st_tagcomAce_posInicial[i][j][1] #etiqueta morfológica do termo com base no Tagger NPLNet
            qtdeTermos = qtdeTermos + 1
            listaAux = []
            for linhaW in st_WordNet:
                
                if etiqueta == 'N' and linhaW[1] == 'Substantivo' and radical in linhaW[2:]:
                    listaAux.append(linhaW)

                elif (etiqueta == 'V' or etiqueta == 'VAUX') and linhaW[1] == 'Verbo' and radical in linhaW[2:]:
                    listaAux.append(linhaW)
                
                elif etiqueta == 'ADJ' and linhaW[1] == 'Adjetivo' and radical in linhaW[2:]:
                    listaAux.append(linhaW)
                    
                    
            dicSin[termo] = listaAux
#         pprint(dicSin)
        print qtdeTermos
        qtdeTermosTotal = qtdeTermos + qtdeTermosTotal
#         exit()
    print qtdeTermosTotal       
    
    print "FIM DA NORMALIZAÇAO"
    
    duration = time.time() - start
    stats = yappi.get_func_stats()
    stats.save('normalizacao.out', type = 'callgrind')
     
    
#########################################################################################
### REALIZA A TROCA DO TERMOS SINÔNIMOS POR UM ÚNICO TERMO E MONTA OS NOVOS            ##
### POSICIONAMENTOS INICIAIS PARA ANÁLISE DE SIMILARIDADE NA VARIÁVELS norm_porInicial ##
#########################################################################################    
    
    for i in sw_tagcomAce_posInicial:
        print i
    
    
    
    
    
    
    
    
    
    return norm_posInicial



















