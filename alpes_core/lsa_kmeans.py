# -*- coding: utf-8 -*-

#Kmeans
import collections
from sklearn.cluster import KMeans

#LSA
from gensim import corpora, models, similarities
from collections import defaultdict
import logging
from pprint import pprint
from alpes_core.pre_text_process import removeA, removePontuacao
from nltk.corpus import stopwords


def LSA_Kmeans(clusters, textoTreinamento, nomeUsuarios, textoComparacao=None):
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


    # To obtain similarities of our query document against the indexed documents:
    # perform a similarity query against the corpus
    sims = indexComp[query]
    
#     pprint(sims)   
        

    ##########################################################################################
    # JUNÇÃO COM K-MEANS PARA REALIZAR AGRUPAMENTOS                                          #
    ##########################################################################################

    ##Valor ideal, após experimentos = 100000
    km_model = KMeans(n_clusters=clusters, n_init=100000)

    km_model.fit_transform(sims)
    
    clustering = collections.defaultdict(list)
 
    for idx, label in enumerate(km_model.labels_):
        clustering[label].append(idx)
 
    print "clustering _LSA_KMEANS"
    pprint(clustering)
    
    print len(clustering)
    
    for i in range(len(clustering)):
        for j in clustering[i]:
            print "grupo", i
            print j, nomeUsuarios[j]
            print textoComparacao[j]
            
    
    return clustering    
    