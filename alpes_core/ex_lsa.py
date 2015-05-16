# -*- coding: utf-8 -*-
from alpes_core.clusterArgInicial import clusterArgInicial
from alpes_core.pre_text_process import removeA

from nltk.corpus import stopwords
from numpy.f2py.rules import aux_rules
from sklearn.metrics.pairwise import cosine_similarity

# dadosTratados = clusterArgInicial('1472')
# 
# #dados necessários
# posIni = dadosTratados[1] 
# st_posInicial = dadosTratados[4]
# alunos = dadosTratados[3]

#COPIAR O CÓDIGO ABAIXO PARA VIEWS E REALIZAR TESTES
##########################################################################################
# LATENTIC SEMANTIC ANALASYS - WITH GENSIN BIB  #
##########################################################################################
from gensim import corpora, models, similarities
from collections import defaultdict
import logging
from pprint import pprint
from datetime import datetime


def similaridade_lsa(posIni, alunos):
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    
    
    #CORPUS = documents
    lsa_posInicial = [] #contém os dados do posInicial sem acentuação!!!
    
    #REMOVE ACENTOS!
    #posIni já é tratada e não tem as tags html
    for i in posIni:
        aux = removeA(i)
        lsa_posInicial.append(aux)
    
    # print lsa_posInicial
    
    
    documents = lsa_posInicial
    
    #remoção de stopwords
    stoplist = stopwords.words('portuguese')
    texts = [[word for word in document.lower().split() if word not in stoplist] \
             for document in documents]
    
    # print texts
    
    frequency = defaultdict(int)
    
    for text in texts:
        for token in text:
            frequency[token] += 1
    
    texts = [[token for token in text if frequency[token] > 1]\
             for text in texts]
    
    # pprint(texts)
    
    dicionario = corpora.Dictionary(texts)
    # dicionario.save('/home/panceri/git/alpes_v1/arquivos/dicionario.dict')
    
    # print dicionario
    #212 termos unicos = cada documentos é representado por 212 numeros
    #212-D vetores
    
    # print dicionario.token2id
    
    corpus = [dicionario.doc2bow(texto) for texto in texts]
    # corpora.MmCorpus.serialize('/home/panceri/git/alpes_v1/arquivos/corpus.mm', corpus)
     
    # corpus = corpora.MmCorpus('/home/panceri/git/alpes_v1/arquivos/corpus.mm')
    
    #TF-IDF
    tfidf = models.TfidfModel(corpus, normalize=True) #inicializa o modelo
    
    corpus_tfidf = tfidf[corpus]
    
    lsi = models.LsiModel(corpus_tfidf, id2word=dicionario,num_topics=len(dicionario))
    corpus_lsi = lsi[corpus_tfidf] 
    # lsi.save('/home/panceri/git/alpes_v1/arquivos/model.lsi')
    
    for doc in corpus_lsi:
        print doc 
    
    # doc = lsa_posInicial
    vec_bow = [dicionario.doc2bow(texto) for texto in texts]
    vec_lsi = lsi[vec_bow]
    # print list(vec_lsi)
    
    index = similarities.MatrixSimilarity(lsi[corpus])
    # index.save('/home/panceri/git/alpes_v1/arquivos/indice.index')
    
    # pprint(list(index))
    
    sims = index[vec_lsi]
    # pprint(list(enumerate(sims)))
    
    # pprint(sims)
    
    now = datetime.now()
    
    resultado = open("/home/panceri/git/alpes_v1/arquivos/resultado"+now.__str__()+".txt", "w")
    resultados = []
    for i in range(0, len(sims)):
        aux = sorted(sims[i], reverse=True)
        for x in range(len(aux)):
            for y in range(x+1, len(aux)):
                str_aux = ""
                str_aux = alunos[x] +" " + aux[y].__str__() + "% similar" + alunos[y]
                resultados.append(str_aux)
                resultado.write(alunos[x] +" " + aux[y].__str__() + "% similar" + alunos[y] + "\n")
    
    resultado.close()
    
    pprint(resultados)

    return resultados   
            
    


##########################################################################################