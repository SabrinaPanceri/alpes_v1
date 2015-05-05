# -*- coding: utf-8 -*-
# calculo do TF-IDF das palavras que estão no posicionamento final

from nltk import RegexpTokenizer, bigrams, trigrams
import re, math
from alpes_core.clusterArgFinal import sw_posFinal, sw_tese, tese
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from alpes_core.naoUtilizados.similarity import similaridade, simple_cosine_sim
from nltk.stem import RSLPStemmer 


palavras = RegexpTokenizer("[\w’]+", flags=re.UNICODE)
 
 
def freq(word, doc):
#     print "freq(word)" , doc.count(word)
    return doc.count(word)
 
 
def word_count(doc):
#     print "word_count(doc)",len(doc)
    return len(doc)
 
 
def tf(word, doc):
#     print "TF", (freq(word, doc) / float(word_count(doc)))
    return (freq(word, doc) / float(word_count(doc)))
 
 
def num_docs_containing(word, list_of_docs):
    count = 0
    for document in list_of_docs:
        if freq(word, document) > 0:
            count += 1
#     print "num_docs_containing",1 + count 
    return 1 + count
 
 
def idf(word, list_of_docs):
#     print "IDF", math.log(len(list_of_docs) /
#             float(num_docs_containing(word, list_of_docs)))
    return math.log(len(list_of_docs) /
            float(num_docs_containing(word, list_of_docs)))
 
 
def tf_idf(word, doc, list_of_docs):
#     print "tf_idf",(tf(word, doc) * idf(word, list_of_docs)) 
    return (tf(word, doc) * idf(word, list_of_docs))
 
#Compute the frequency for each term.
vocabulary = []
docs = {}

for pos in (sw_posFinal):
   
    tokens = palavras.tokenize(pos)
    
    tokens = [token.lower() for token in tokens if len(token) > 2]
 
    final_tokens = []
    final_tokens.extend(tokens)
    docs[pos] = {'freq': {}, 'tf': {}, 'idf': {},
                        'tf-idf': {}, 'tokens': []}
 
    for token in final_tokens:
        #The frequency computed for each pos
        docs[pos]['freq'][token] = freq(token, final_tokens)
        #The term-frequency (Normalized Frequency)
        docs[pos]['tf'][token] = tf(token, final_tokens)
        docs[pos]['tokens'] = final_tokens
 
    vocabulary.append(final_tokens)
 
for doc in docs:
    for token in docs[doc]['tf']:
        #The Inverse-Document-Frequency
        docs[doc]['idf'][token] = idf(token, vocabulary)
        #The tf-idf
        docs[doc]['tf-idf'][token] = tf_idf(token, docs[doc]['tokens'], vocabulary)

#Now let's find out the most relevant words by tf-idf.
words = {}
for doc in docs:
    for token in docs[doc]['tf-idf']:
        if token not in words:
            words[token] = docs[doc]['tf-idf'][token]
        else:
            if docs[doc]['tf-idf'][token] > words[token]:
                words[token] = docs[doc]['tf-idf'][token]

# for item in sorted(words.items(), key=lambda x: x[1], reverse=True):
#     print "%f <= %s" % (item[1], item[0])