# -*- coding: utf-8 -*-
##################################################################
### CÓDIGO DESENVOLVIDO POR SABRINA SIQUEIRA PANCERI            ##
### PROTÓTIPO DE SUA  DISSERTAÇÃO DE MESTRADO                   ##
### ESSE CÓDIGO PODE SER COPIADO, ALTERADO E DISTRIBUÍDO        ##
### DESDE QUE SUA FONTE SEJA REFERENCIADA                       ##
### PARA MAIS INFORMAÇÕES, ENTRE EM CONTATO ATRAVÉS DO EMAIL    ##
### SABRINASPANCERI@GMAIL.COM                                   ##
##################################################################



##########################################################################################
#                     LATENTIC SEMANTIC ANALASYS - WITH GENSIN BIB                       #
##########################################################################################
from gensim import corpora, models, similarities
from collections import defaultdict
import logging
from pprint import pprint
from datetime import datetime
from alpes_core.textProcess import removeA, removePontuacao
from nltk.corpus import stopwords
from gensim.models import lsimodel
from gensim.models.rpmodel import RpModel
import os


def similaridade_lsa(textoTreinamento, nomeUsuarios, textoComparacao=None):
    
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    ##########################################################################################
    #  PRÉ-PROCESSAMENTO DO TEXTO ENVIADO PARA CRIAÇÃO DO DICIONÁRIO DE RELACOES SEMANTICAS  #
    ##########################################################################################    
    
    #UTILIZA AS FUNCOES removeA e removePontuacao PARA TRATAR textoTreinamento 
    textoTrein = [removeA(removePontuacao(i)) for i in textoTreinamento] 
    #print textoTrein
    
    textoComp = [removeA(removePontuacao(i)) for i in textoComparacao]
    
    #CARREGA A LISTA DE STOPWORDS DA NLTK    
    stop = stopwords.words('portuguese')
    #RETIRA OS ACENTOS DA LISTA DE STOPWORDS   
    stoplist = [(removeA(s)) for s in stop ]
#     print stoplist
    
    #REMOVE AS STOPWORDS E PALAVRAS COM MENOS DE 3 CARACTERES
    textoTrein = [[word for word in document.lower().split() if word not in stoplist and len(word) > 3] \
             for document in textoTrein]
#     print sw_textoTrein

    textoComp = [[word for word in document.lower().split() if word not in stoplist and len(word) > 3] \
             for document in textoComp]
#     print textoComp
##############################################################################################
#     INICIO DE APLICACAO DO LSA - CRIANDO O DICIONARIO DE TERMOS/FREQUENCIA                 #
##############################################################################################

    #DEFINE FREQUENCIA COMO UMA VARIAVEL DO TIPO DICIONARIO DE INTEIROS
    frequencia = defaultdict(int)
    
    #ARMAZENA A QUANTIDADE DE REPETIÇÕES DE UM TERMO EM TODOS OS DOCUMENTOS DA COLECAO
    for t in textoTrein:
        for token in t:
            frequencia[token] += 1
#     pprint(frequencia)
   
    #PALAVRAS COM FREQUENCIA 1 NÃO SÃO IMPORTANTES, POIS NÃO POSSUEM RELACOES DE CO-OCORRENCIA
    #Remove todas as palavras que apareceram apenas 1 vez durante a contagem
    textoTrein = [[token for token in palavra if frequencia[token] > 1]\
             for palavra in textoTrein]
#     pprint(textoTrein)
    
    
    ##########################################################################################
    # Dictionary encapsulates the mapping between normalized words and their integer ids.    #
    # The main function is `doc2bow`, which converts a collection of words to its            #
    # bag-of-words representation: a list of (word_id, word_frequency) 2-tuples.             #
    ##########################################################################################
    dicionario = corpora.Dictionary(textoTrein)
#     print dicionario
    
    # Armazena o ID das palavras que aparecem apenas 1 vez nos textos
    once_ids = [tokenId for tokenId,docfreq in dicionario.dfs.iteritems() if docfreq == 1]
#     print once_ids
    
    #remove todas as palavras com frequencia = 1
    dicionario.filter_tokens(once_ids)
    
    #reorganiza o dicionario, realocando os dados para os indices que foram removidos
    dicionario.compactify()
    
#     print dicionario.token2id # token -> tokenId
#     print dicionario.dfs # document frequencies: tokenId -> in how many documents this token appeared
    
    # Atribui a corpus_textoTrein o textoTrein no formato "bag-of-words"
    # The main function is `doc2bow`, which converts a collection of words to its
    # bag-of-words representation: a list of (word_id, word_frequency) 2-tuples.
    corpus_textoTrein = [dicionario.doc2bow(texto) for texto in textoTrein]
#     pprint(corpus_textoTrein)
    
    corpus_textoComp = [dicionario.doc2bow(textoC) for textoC in textoComp]
#     pprint(corpus_textoComp)
    ##########################################################################################
    # MODELO DE TRANSFORMACAO - BAG-OF-WORDS PARA TF-IDF                                     #
    ##########################################################################################
    
    # TRANSFORMA corpus_textoTrein (bag-of-words) 
    # PARA tfidf_TextoTrein (frequencia termos x inverso da freq no documento 
    tfidf_TextoTrein = models.TfidfModel(corpus=corpus_textoTrein)
#     print tfidf_TextoTrein
    
    #USA O posIni PARA GERAR A MATRIZ DE COMPARACAO COM OS DADOS DO DICIONARIO
    corpus_tfidf_TextoTrein = tfidf_TextoTrein[corpus_textoComp]
#     print list(corpus_tfidf_TextoTrein)
    
    #TRANSFORMA A MATRIZ TF-IDF 
    modelo_lsa = models.LsiModel(corpus_tfidf_TextoTrein, id2word=dicionario,num_topics=len(dicionario))
    
    #TRANSFORMA OS DADOS DE TREINAMENTO EM LSA
#     corpus_lsi = modelo_lsa[corpus_tfidf_TextoTrein] 
    
#     for doc in corpus_lsi:
#         pprint(doc)
    
    query = []

    for q in textoComparacao:
        vec_bow = dicionario.doc2bow(q.lower().split())
        vec_lsi = modelo_lsa[vec_bow] #convert a query de comparação num espaço LSI
        query.append(vec_lsi)         
#     print "query"
#     pprint(query)
    
    #TRANSFORMA corpus_textoComp num espaço LSA e indexa 
    indexComp = similarities.MatrixSimilarity(modelo_lsa[corpus_textoComp])
#     print "indexComp"
#     pprint(list(indexComp))


    # To obtain similarities of our query document against the nine indexed documents:
    # perform a similarity query against the corpus
    sims = indexComp[query]
#     pprint(list(enumerate(sims)))

    
    now = datetime.now()
    resultado = open(os.path.join(os.path.dirname(__file__),"../arquivos/resultado"+now.__str__()+".txt"), "w")
    resultados = []
    
    for i in range(0, len(sims)):
        aux = sims[i]
#         print "sorted",sorted(sims[i], reverse=True)
#         print i, aux 
        for y in range(i+1, len(aux)):
            str_aux = [nomeUsuarios[i] +" " + aux[y].__str__() + "% similar" + nomeUsuarios[y]]
#             print str_aux
#             resultados.append(str_aux)
            resultados.append([aux[y],nomeUsuarios[i],nomeUsuarios[y]])
            resultado.write(nomeUsuarios[i] +" " + aux[y].__str__() + "% similar" + nomeUsuarios[y] + "\n")
# #     
    resultado.close()
#     print "resultados"
#     pprint(resultados)

    return resultados   
            
    


##########################################################################################
