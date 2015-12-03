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


def normalizacaoWordnet(listaAdjetivos, listaSubstantivos, listaVerbos,listaOutros, st_tagcomAce_posInicial):

################################################################
### MEDIÇÃO DE PROCESSAMENTO / DESEMPENHO / REQUISIÕES #########
################################################################
    yappi.set_clock_type('cpu')
    yappi.start(builtins=True)      
    start = time.time() 
    
#########################################################################################
### BUSCA PELOS TERMOS SINÔNIMOS EM st_WordNet E MONTA O DICIONÁRIO COM AS RELAÇÕES    ##
#########################################################################################    
    qtdeTermosTotal = 0
    dicionario = {} ##guarda todas as relações de sinonímia para os termos de cada argumentação
    
    print "BUSCA PELOS TERMOS SINÔNIMOS EM st_WordNet E MONTA O DICIONÁRIO COM AS RELAÇÕES"
    
    ## pega cada argumento (21 no total)
    for iST in range(len(st_tagcomAce_posInicial)):
        qtdeTermos = 0
        
        for jST in range(len(st_tagcomAce_posInicial[iST])):
            qtdeTermos = qtdeTermos + 1
            radical = st_tagcomAce_posInicial[iST][jST][0] #termo reduzido ao seu radical de formação (aplicação de stemmer - RSLP)
            etiqueta = st_tagcomAce_posInicial[iST][jST][1] #etiqueta morfológica do termo com base no Tagger NPLNet

            if etiqueta == "N":
                listSub = []
                for i in range(len(listaSubstantivos)):
                    for aux_radical in listaSubstantivos[i][2]:
                        if aux_radical == radical:
                            listSub.append(listaSubstantivos[i][2])
                    dicionario[radical] = listSub

            elif etiqueta == "V" or etiqueta == "VAUX":
                listVerb = []
                for i in range(len(listaVerbos)):
                    for aux_radical in listaVerbos[i][2]:
                        if aux_radical == radical:
                            listVerb.append(listaVerbos[i][2])
                    dicionario[radical] = listVerb
                            
                        
            elif etiqueta == "ADJ":
                listAdj = []
                for i in range(len(listaAdjetivos)):
                    for aux_radical in listaAdjetivos[i][2]:
                        if aux_radical == radical:
                            listAdj.append(listaAdjetivos[i][2])
                    dicionario[radical] = listAdj
                            
            else:
                listOutros = []
                for i in range(len(listaOutros)):
                    for aux_radical in listaOutros[i][2]:
                        if aux_radical == radical:
                            listOutros.append(listaOutros[i][2])
                    dicionario[radical] = listOutros
                            

        qtdeTermosTotal = qtdeTermosTotal + qtdeTermos
                            
    print "Dicionário de sinônimos pronto!!"
    print "Total de termos analisados: ", qtdeTermosTotal
    
#     pprint(dicionario)
#     exit()
                
#########################################################################################
### REALIZA A TROCA DO TERMOS SINÔNIMOS POR UM ÚNICO TERMO E MONTA OS NOVOS            ##
### POSICIONAMENTOS INICIAIS PARA ANÁLISE DE SIMILARIDADE NA VARIÁVELS norm_porInicial ##
#########################################################################################
    norm_posInicial = []    
    
    print "TROCA DE TERMOS"
    aux = ""
    listAux = []
    
    
    print len(dicionario['exclud'])
    print "exclud"
    print dicionario['exclud']
    
    
    for idST in range(len(st_tagcomAce_posInicial)):
        
        for tupla in st_tagcomAce_posInicial[idST]:
            print "segundo for"
             
            print tupla
            termoStr = tupla[0]
            
            print "buscar termo dentro do dicionário"
            
            ## tratar casos aonde não são encontrados sinônimos para o termo
            ## exemplo dicionario['exclud']
            ## colocar numa condicional 
            
            
            for valores in dicionario.itervalues():
#                 print valores
                
                for valor in valores:
                    
                    for pal in valor:
                        
                        if pal not in listAux:
                    
                            if termoStr == pal:
                                print "valor", valor
                                listAux.append(termoStr)
            
            
            print st_tagcomAce_posInicial[0]    
            print len(listAux)
            print listAux
         
            exit()
            
            
        #norm_posInicial.append(listAux)

        #exit()
        
    #norm_posInicial.append(listAux)
            
#     print "normalizado"
#     #print norm_posInicial
#     print len(norm_posInicial)
    
#     for i in range(len(norm_posInicial)):
#         print len(norm_posInicial[i])
        
    exit()
        
    
    
    
    

################################################################
### MEDIÇÃO DE PROCESSAMENTO / DESEMPENHO / REQUISIÕES #########
################################################################    
    duration = time.time() - start
    stats = yappi.get_func_stats()
    stats.save('normalizacaoWordnet.out', type = 'callgrind')
    


#########################################################################################   
    return norm_posInicial



















