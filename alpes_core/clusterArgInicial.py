
# -*- coding: utf-8 -*-
##################################################################
### CÓDIGO DESENVOLVIDO POR SABRINA SIQUEIRA PANCERI            ##
### PROTÓTIPO DE SUA  DISSERTAÇÃO DE MESTRADO                   ##
### ESSE CÓDIGO PODE SER COPIADO, ALTERADO E DISTRIBUÍDO        ##
### DESDE QUE SUA FONTE SEJA REFERENCIADA                       ##
### PARA MAIS INFORMAÇÕES, ENTRE EM CONTATO ATRAVÉS DO EMAIL    ##
### SABRINASPANCERI@GMAIL.COM                                   ##
##################################################################


#############################################################################################################
# Imports obrigatorios
import HTMLParser
import codecs
import re
import nlpnet
from django.db import connection
from alpes_core.textProcess import removeStopWords, removePontuacao, limpaCorpus,\
    removeA, removeNum, removeSE
from nltk.stem import RSLPStemmer
from pprint import pprint
from alpes_core.normalizacaoWordnet import normalizacaoWordnet

import yappi
import time
import os

# import nltk, sys
# from alpes_core.textProcess import stemming
# from nltk.corpus import floresta
# from nltk.probability import FreqDist
# from nltk import word_tokenize as wt


#############################################################################################################
### INDICA A BASE DE DADOS PARA FAZER A CLASSIFICACAO SINTATICA
### USO DO POS TAGGER DA NLPNET 
### COPIAR PARA O SERVIDOR A PASTA NLPNET-DATA
### COLOCAR CAMINHO CORRETO DENTRO DO SERVIDOR!!!
#nlpnet.set_data_dir('/home/panceri/nlpnet-data/pos-pt')
nlpnet.set_data_dir(os.path.join(os.path.dirname(__file__),'../../../nlpnet-data'))

#############################################################################################################

#############################################################################################################

#############################################################################################################
## Desenvolvimento da lógica de execução do Núcleo de processamento do Alpes                                #
## Aplicação das técnicas de pré-processamento textual a fim de ajudar no processo de comparação e busca    #
## de textos similares                                                                                      #
## Técnicas desenvolvidas                                                                                   #
## 1 - Case folding                                                                                         #
## 2 - Troca de caracteres acentuados por caracteres não acentuados                                         #
## 3 - Remoção pontuações                                                                                   #
## 4 - Remoção de stopwords                                                                                 #
## 5 - Stemming                                                                                             #
## 6 - Normalização                                                                   #
#############################################################################################################

##############################################################################################################
## DESENVOLVIMENTO DA FERRAMENTA "GRUPOS DE ARGUMENTAÇÃO" - PROTÓTIPO ALPES
## UTILIZAÇÃO DA ARGUMENTAÇÃO INICIAL PARA CRIAR GRUPOS DE ALUNOS QUE INICIARAM O DEBATE COM CONHECIMENTOS 
## SIMILARES SOBRE A TESE 
##############################################################################################################  

def clusterArgInicial(idtese):

    #Variaveis e funçoes para conexação com o banco de dados do Debate de Teses
    cursor = connection.cursor()
    cursor2 = connection.cursor()

    cursor.execute("select distinct `usr`.`primeironome` as `name`, `arg`.`argumento` AS `posicionamentoinicial` from ((((`argumento` `arg` join `revisao` `rev`) join `replica` `rep`) join `posicionamento` `pos`) join `argumentador` `urg`)join `usuario` `usr`  where ((`arg`.`tese_idtese` = " + idtese + "  ) and (`rev`.`argumento_idargumento` = `arg`.`idargumento`) and (`rep`.`revisao_idrevisao` = `rev`.`idrevisao`) and (`arg`.`argumentador_idargumentador` = `pos`.`argumentador_idargumentador`) and (`arg`.`tese_idtese` = `pos`.`tese_idtese`) and (`arg`.`posicionamentoinicial` is not null) and (`arg`.`argumentador_idargumentador` = `urg`.`idargumentador`) and(`urg`.`usuario_idusuario` = `usr`.`idusuario`) and (`pos`.`posicionamentofinal` is not null))")
    cursor2.execute("select tese from tese where idtese="+ idtese)
    
    #Variavel e função para tratar tags html e acentos com codificação ISO
    h = HTMLParser.HTMLParser()
    
    #dados retirados da consulta ao banco
    dadosSql = cursor.fetchall()
    textotese = cursor2.fetchall()
    
    #listas para tratar os dados iniciais
    usu = []
    posInicial = []
    dados = []
    tese = []
    
    #lista com dados pos tagger
    tag_posInicial = []
    tag_comAce_posInicial = []
    
    #lista com dados após a remoção das stopwords
    sw_tese = []
    sw_posInicial = []
    aux_usu = []
    sw_tagPosInicial = [] #texto marcado e sem stopwords
    sw_tagcomAce_posInicial = [] #texto COM ACENTOS marcado e sem stopwords 


    #lista com dados após a aplicação de Stemming
    st_posInicial = []
    st_tese = []
    st_tagPosInicial = [] #texto marcado, sem stopwords e com stemmer aplicado
    st_tagcomAce_posInicial = [] #texto COM ACENTOS marcado, sem stopwords e com stemmer aplicado
    
#############################################################################################################    
    #LISTA COM OS POSICIONAMENTOS INICIAIS APÓS APLICAÇÃO DA NORMALIZAÇAÕ
    posInicial_Normalizado = []
      

#############################################################################################################    
#Aplicacao de Case Folding

    for d in dadosSql:
        dados.append([re.sub('<[^>]*>', '', h.unescape(d[0])).lower(),
                      re.sub('<[^>]*>', '', h.unescape(d[1])).lower()])

    for t in textotese:
        tese.append(re.sub('<[^>]*>', '', h.unescape(t[0])).lower())
            

    #Colocando os textos de posicionamento inicial em numa lista separada
    for i in dados:
        x = 0
        usu.append(i[x].upper())
        posInicial.append(i[x+1].lower()) #lista com o posicionamento Inicial

#############################################################################################################
### Classificacao das palavras de acordo com sua classe gramatical
### Utilizacao do postagger NLPNET
### http://nilc.icmc.usp.br/nlpnet/index.html#
    
    tagger = nlpnet.POSTagger()
    
    semAce_posInicial = [] #armazena o posInicial apenas sem acentos, sem pontuações, sem endereço web e sem numeros 
    comAce_posInicial = [] #armazena o posInicial apenas COM acentos, sem pontuações, sem endereço web e sem numeros
    
    for i in posInicial:
        semAce_posInicial.append(removePontuacao(removeA(removeNum(removeSE((i))))))
    
    for i in semAce_posInicial:
        tag_posInicial.append(tagger.tag(i))
        
    for i in posInicial:
        comAce_posInicial.append(removePontuacao(removeNum(removeSE((i)))))
        
    for i in comAce_posInicial:
        tag_comAce_posInicial.append(tagger.tag(i))

#############################################################################################################
### REMOCAO DE STOPWORDS
### Remocao dos termos de acordo com a NLTK
### Remocao dos termos classificados como artigos, verbos, adverbios, etc...
    
    
    for i in usu:
        aux_usu.append(removeStopWords(i))

    for i in tese:
        sw_tese.append(removeStopWords(i))

    for i in posInicial:
        sw_posInicial.append(removeStopWords(i))
        
    for i in tag_posInicial:
        sw_tagPosInicial.append(limpaCorpus(i))
    
    for i in tag_comAce_posInicial:
        sw_tagcomAce_posInicial.append(limpaCorpus(i))
    

####################################################################################################################################
# Aplicação do RSPL Stemmer para remoção dos afixos das palavras da lingua portuguesa
# Retirando afixos dos textos do posInicial e tese

    
    stemmer = RSLPStemmer()
 
    for i in range(len(sw_posInicial)):
        st_aux = sw_posInicial[i]
        string_aux = ""
        for sufixo in st_aux.split():
            string_aux = string_aux + " " + stemmer.stem(sufixo)
         
        st_posInicial.append(string_aux)

    
    for i in range(len(sw_tese)):
        st_aux = sw_tese[i]
        string_aux = ""
        for sufixo in st_aux.split():
            string_aux = string_aux + " " + stemmer.stem(sufixo)
         
        st_tese.append(string_aux)
        
    for i in range(len(sw_tagPosInicial)):
        termosST = ""
        auxST = []
        for j in range(len(sw_tagPosInicial[i])):
            aux = stemmer.stem(sw_tagPosInicial[i][j][0])
            etiqueta = sw_tagPosInicial[i][j][1]
            termosST = (aux,etiqueta)
            auxST.append(termosST)
        
        st_tagPosInicial.append(auxST)
        
    for i in range(len(sw_tagcomAce_posInicial)):
        termosST = ""
        auxST = []
        for j in range(len(sw_tagcomAce_posInicial[i])):
            aux = stemmer.stem(sw_tagcomAce_posInicial[i][j][0])
            etiqueta = sw_tagcomAce_posInicial[i][j][1]
            termosST = (aux,etiqueta)
            auxST.append(termosST)
        
        st_tagcomAce_posInicial.append(auxST)


    
####################################################################################################################################
### A NORMALIZACAO DE TERMOS REFERE-SE A TECNICA DE TROCAR PALAVRAS SINONIMAS, OU SEJA, QUE TENHAM SIGNIFICADO                    ##
### SEMELHANTE, POR UM UNICO TERMO REPRESENTATIVO NO CORPUS DE ANALISE. DESSA FORMA, É POSSIVEL AUMENTAR O GRAU                   ##
### DE SIMILARIDADE ENTRE OS TEXTOS ANALISADOS ATRAVES DO USO DE TECNICAS DE ANALISE ESTATISTICAS, COMO SIMILA                    ##
### RIDADE DE COSSENOS OU DISTANCIA EUCLIDIANA.                                                                                   ##
####################################################################################################################################   
### A NORMALIZACAO FOI DESENVOLVIDA COM BASE NOS DADOS DISPONIBILIZADOS PELO PROJETO TEP 2.0 DO NILC/USP                          ##
### http://143.107.183.175:21480/tep2/index.htm                                                                                   ##
###                                                                                                                               ## 
### FORMATO DO ARQUIVO                                                                                                            ##
### NUM1. [Tipo] {termos sinonimos} <NUM2>                                                                                        ##
### 263. [Verbo] {consentir, deixar, permitir} <973>                                                                              ##
### NUM1 = NUMERO DA LINHA DE REFERENCIA PARA TERMO SINONIMO                                                                      ##
### NUM2 = NUMERO DA LINHA DE REFERENCIA PARA TERMO ANTONIMO (SENTIDO OPOSTO)                                                     ##
####################################################################################################################################
    
    #abre o arquivo com as relacoes de sinonimia (termos linhaWordNet) e antonimia (termos contrarios)
    #arquivo apenas com termos classificados como substantivos, adjetivos e verbos 
    base_tep = codecs.open('/home/caiovdpvb/git/alpes_v1/base_tep2/base_tep.txt', 'r', 'UTF8')
#     dicionario = open('/home/panceri/git/alpes_v1/base_tep2/dicionarioSinonimos.txt', 'w')
    
    #variavel com conteúdo do arquivo em memoria
    #não imprimir essa variável, MUITO GRANDEE!!!
    wordNet = base_tep.readlines()
    
    #fechar arquivo 
    base_tep.close()
    
####################################################################################################################################
## NORMALIZAÇÃO FEITA COM BASE NOS RADICAIS DE FORMAÇÃO DAS PALAVRAS                                                              ##
## APLICAÇÃO DO RSPL PRIMEIRO PARA DEPOIS BUSCAR NA BASE OS TERMOS SIMILARES                                                      ##
## DENTRO DA BASE_TEP OS TERMOS TAMBÉM FORAM REDUZIDOS AOS SEUS RADICIAIS DE FORMAÇÃO                                             ##
## O DICIONÁRIO ESTÁ COM A REFERÊNCIA PARA A LINHA AONDE ESTÃO OS TERMOS SINÔNIMOS                                                ##
## OS TERMOS SÃO ANALISADOS CONSIDERANDO SUAS ACENTUAÇÕES, PARA APLICAÇÃO CORRETA DO RSLP                                         ##
####################################################################################################################################
    
    yappi.set_clock_type('cpu')
    yappi.start(builtins=True)
    start = time.time()    

    st_WordNetV = [] ##armazena num, tipo, e radical dos sinonimos - APENAS VERBOS
    st_WordNetN = [] ##armazena num, tipo, e radical dos sinonimos - APENAS SUBSTANTIVOS
    st_WordNetA = [] ##armazena num, tipo, e radical dos sinonimos - APENAS ADJETIVOS
    st_WordNetO = [] ##armazena num, tipo, e radical dos sinonimos - APENAS OUTROS
    
    for linhaWordnet in wordNet:
        listaAux = []
        termos = re.findall(r"\{(.*)\}", linhaWordnet)
        num = re.findall(r"([0-9]+)\.", linhaWordnet)
        tipo = re.findall(r"\[(.*)\]", linhaWordnet)
        
        
        if tipo[0] == "Substantivo":
            listaAux.append(num)
            listaAux.append(tipo)
            
            for T in termos:
                aux = T.split()
                auxL = []
                for i in aux:
                    aux1 = i.replace(",", "")
                    dadosStem = stemmer.stem(aux1)
                    auxL.append(dadosStem)
                listaAux.append(auxL)
            st_WordNetN.append(listaAux)
            
        elif tipo[0] == "Verbo":
            listaAux.append(num)
            listaAux.append(tipo)
            
            for T in termos:
                aux = T.split()
                auxL = []
                for i in aux:
                    aux1 = i.replace(",", "")
                    dadosStem = stemmer.stem(aux1)
                    auxL.append(dadosStem)
                listaAux.append(auxL)
            st_WordNetV.append(listaAux)
        
        elif tipo[0] == "Adjetivo":
            listaAux.append(num)
            listaAux.append(tipo)
            
            for T in termos:
                aux = T.split()
                auxL = []
                for i in aux:
                    aux1 = i.replace(",", "")
                    dadosStem = stemmer.stem(aux1)
                    auxL.append(dadosStem)
                listaAux.append(auxL)
            st_WordNetA.append(listaAux)
        else:
            listaAux.append(num)
            listaAux.append(tipo)
            
            for T in termos:
                aux = T.split()
                auxL = []
                for i in aux:
                    aux1 = i.replace(",", "")
                    dadosStem = stemmer.stem(aux1)
                    auxL.append(dadosStem)
                listaAux.append(auxL)
            st_WordNetO.append(listaAux)
            

 
    duration = time.time() - start
    stats = yappi.get_func_stats()
    stats.save('stemmWordNet.out', type = 'callgrind')
    
####################################################################################################################################
### A ANÁLISE É REALIZADA COM BASE NO TEXTO SEM A EXCLUSÃO DOS ACENTOS                                                            ##
### POIS AO EXCLUÍ-LOS A REDUÇÃO AO RADICAL DE FORMAÇÃO (APLICAÇÃO DO RSLP) É PREJUDICADA                                         ##
### OS TESTES REALIZADOS MOSTRARAM QUE ESSA É UMA MELHOR ABORDAGEM, UMA VEZ QUE NOSSOS TEXTOS SÃO PEQUENOS                        ##
### E PRECISAMOS CHEGAR O MAIS PRÓXIMO POSSÍVEL SEM CONSIDERAR SEUS SENTIDOS E/OU CONTEXTOS                                       ##
####################################################################################################################################
    yappi.set_clock_type('cpu')
    yappi.start(builtins=True)
    start = time.time()    
    
    posInicial_Normalizado = normalizacaoWordnet(st_WordNetA, st_WordNetN, st_WordNetV, st_WordNetO, st_tagcomAce_posInicial)
    
    duration = time.time() - start
    stats = yappi.get_func_stats()
    stats.save('normalizacaoWordnet.out', type = 'callgrind')


####################################################################################################################################

#retorno da função - usado na views.py para alimentar o template debate.html
#passar parametros que devem ser apresentados na templates debate.html
    return [st_tese, posInicial, sw_tese, aux_usu, st_posInicial, tese, posInicial_Normalizado]


####################################################################################################################################













  
