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
from datetime import datetime
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
nlpnet.set_data_dir('/home/panceri/nlpnet-data/')

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
## 6 - Normalização (em finalizacao!)                                                                       #
#############################################################################################################

##############################################################################################################
## DESENVOLVIMENTO DA FERRAMENTA "GRUPOS DE ARGUMENTAÇÃO" - ARTIGO SBIE 2015
## UTILIZAÇÃO DO POSICIONAMENTO INICIAL PARA CRIAR GRUPOS DE ALUNOS QUE INICIARAM O DEBATE COM CONHECIMENTOS 
## SIMILARES SOBRE A TESE 
##############################################################################################################  

def clusterArgInicial(idtese):
    inicio = datetime.now()
    print inicio,"clusterArgInicial"
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
    #DICIONÁRIO COM OS TERMOS NA FORMA DA RADICAL E RELACIONADOS AO NUMERO DA LINHA DOS SINONIMOS COM BASE
    # NO ARQUIVO DA WORDNET
    dicSin = {}
      

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
#     pprint(semAce_posInicial)
    
    for i in semAce_posInicial:
        tag_posInicial.append(tagger.tag(i))
        
    for i in posInicial:
        comAce_posInicial.append(removePontuacao(removeNum(removeSE((i)))))
        
    for i in comAce_posInicial:
        tag_comAce_posInicial.append(tagger.tag(i))

#############################################################################################################
### REMOCAO DE STOPWORDS
### Remocao dos termos de acordo com a NLTK
### Remocao dos termos classificados como artigos, verbos, adjetivos, etc...
    
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
    
#     pprint(sw_tagPosInicial)
#     print len(sw_tagPosInicial)

#############################################################################################################
# Aplicação do RSPL Stemmer para remoção dos afixos das palavras da lingua portuguesa
# Retirando afixos dos textos do posInicial e tese
## FOI NECESSÁRIO RETIRAR OS ACENTOS DOS TERMOS DOS ARQUIVOS COM AS REGRAS DE FORMAÇÃO ## 
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
#         pprint(sw_tagPosInicial[i])
        termosST = ""
        auxST = []
        for j in range(len(sw_tagPosInicial[i])):
            aux = stemmer.stem(sw_tagPosInicial[i][j][0])
            etiqueta = sw_tagPosInicial[i][j][1]
            termosST = (aux,etiqueta)
            auxST.append(termosST)
        
        st_tagPosInicial.append(auxST)
        
    for i in range(len(sw_tagcomAce_posInicial)):
#         pprint(sw_tagPosInicial[i])
        termosST = ""
        auxST = []
        for j in range(len(sw_tagcomAce_posInicial[i])):
            aux = stemmer.stem(sw_tagcomAce_posInicial[i][j][0])
            etiqueta = sw_tagcomAce_posInicial[i][j][1]
            termosST = (aux,etiqueta)
            auxST.append(termosST)
        
        st_tagcomAce_posInicial.append(auxST)
    
#     pprint(st_tagPosInicial)
#     print len(st_tagPosInicial)
#     exit()
    
#############################################################################################################
# PROCESSO DE NORMALIZAÇÃO 
# Troca de termos por seus sinonimos com base na WordNet.BR
# http://143.107.183.175:21480/tep2/index.htm
## NORMALIZAÇÃO FEITA COM BASE NOS RADICAIS DE FORMAÇÃO DAS PALAVRAS
## APLICAÇÃO DO RSPL PRIMEIRO PARA DEPOIS BUSCAR NA BASE OS TERMOS SIMILARES
## DENTRO DA BASE_TEP OS TERMOS TAMBÉM FORAM REDUZIDOS AOS SEUS RADICIAIS DE FORMAÇÃO
## O DICIONÁRIO ESTÁ COM A REFERÊNCIA PARA A LINHA AONDE ESTÃO OS TERMOS SINÔNIMOS
## OS TERMOS SÃO ANALISADOS CONSIDERANDO SUAS ACENTUAÇÕES, PARA APLICAÇÃO CORRETA DO RSLP
#############################################################################################################   
    qtdeTermos = 0
    for i in range(len(st_tagcomAce_posInicial)):
#         print sw_tagcomAce_posInicial[i]
        qtdeTermos = 0
#         print datetime.now()
        for j in range(len(st_tagcomAce_posInicial[i])):
            termo = sw_tagcomAce_posInicial[i][j][0] #termo original digitado pelo aluno
            radical = st_tagcomAce_posInicial[i][j][0] #termo reduzido ao seu radical de formação (aplicação de stemmer - RSLP)
            etiqueta = st_tagcomAce_posInicial[i][j][1] #etiqueta morfológica do termo com base no Tagger NPLNet
#             print termo, radical, etiqueta
            normalizacaoWordnet(dicSin, termo, radical, etiqueta)
            qtdeTermos = qtdeTermos + 1
#         print qtdeTermos
#         print datetime.now()
#         pprint(dicSin)
        

    
#         pprint(dicSin)
#     print qtdeTermos
#     print datetime.now()
#         exit()

#############################################################################################################
### IMPLEMENTAÇÃO INICIAL TENDO POR BASE A ANÁLISE DOS TEXTOS SEM ACENTOS
### SE UTILIZAR A APLICAÇÃO DO RSLP PRIMEIRO, NÃO PRODUZ BONS RESULTADOS
### SE BUSCAR COM BASE NO TERMO, PODE SER UTILIZADO, POIS A COMPARAÇÃO NÃO É PREJUDICADA
#     for i in range(len(st_tagPosInicial)):
#         for j in range(len(st_tagPosInicial[i])):
#             termo = sw_tagPosInicial[i][j][0] #termo original digitado pelo aluno
#             radical = st_tagPosInicial[i][j][0] #termo reduzido ao seu radical de formação (aplicação de stemmer - RSLP)
#             etiqueta = st_tagPosInicial[i][j][1] #etiqueta morfológica do termo com base no Tagger NPLNet
#             normalizacao(dicSin, termo, radical, etiqueta)
#             normalizacao(dicSin, termo="tempos", radical="temp", etiqueta="N")

#############################################################################################################
# #LSI
#     lsi_posInicial = []
#     for i in range(len(sw_posInicial)):
#         aux = "posIni(%d): %s" %(i, sw_posInicial[i])
#         lsi_posInicial.append(aux)
# 
# 
#     lsi = gensim.models.lsimodel.LsiModel(lsi_posInicial)
# # #     print sw_posInicial
#     lsi.print_topics(10)


#############################################################################################################
### Semantic Role Labeling model 
### http://www.nilc.icmc.usp.br/nlpnet/models.html#srl-portuguese
### Marcacao semantica funcionando. Verificar como usar para melhorar os resultados.
#     srl_tagger = nlpnet.SRLTagger()
#     auxSrl_PosIni = [] 
#     srl_PosIni = [] #posicionamento inicial tagueado com SRL 
#     
#     for i in posInicial:
#         auxSrl_PosIni.append(srl_tagger.tag(i))
#       
#     for aux in auxSrl_PosIni:
#         for j in aux:
#             srl_PosIni.append(j.arg_structures)



#############################################################################################################
#retorno da função - usado na views.py para alimentar o template debate.html
#passar parametros que devem ser apresentados na templates debate.html
    return [st_tese, posInicial, sw_tese, aux_usu, st_posInicial, tese, dicSin]


#############################################################################################################












  
