# -*- coding: utf-8 -*-

from nltk import RegexpTokenizer, bigrams, trigrams
import re, math
from alpes_core.clusterArgFinal import sw_posFinal
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import math


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
all_tips = []

for pos in (sw_posFinal):
#     print "sw_posFinal", sw_posFinal
    
    tokens = palavras.tokenize(pos)
    
#     print "tokens", tokens
    
    bi_tokens = bigrams(tokens)
    tri_tokens = trigrams(tokens)
    
    tokens = [token.lower() for token in tokens if len(token) > 2]
 
    bi_tokens = [' '.join(token).lower() for token in bi_tokens]
 
    tri_tokens = [' '.join(token).lower() for token in tri_tokens]
 
 
#     print "TOKENS", tokens
#     print "BI-TOKENS", bi_tokens
#     print "TRI-TOKENS", tri_tokens
 
    final_tokens = []
    final_tokens.extend(tokens)
    final_tokens.extend(bi_tokens)
    final_tokens.extend(tri_tokens)
    docs[pos] = {'freq': {}, 'tf': {}, 'idf': {},
                        'tf-idf': {}, 'tokens': []}
 
    for token in final_tokens:
        #The frequency computed for each pos
        docs[pos]['freq'][token] = freq(token, final_tokens)
        #The term-frequency (Normalized Frequency)
        docs[pos]['tf'][token] = tf(token, final_tokens)
        docs[pos]['tokens'] = final_tokens
 
    vocabulary.append(final_tokens)
#     print vocabulary
 
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
    
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(docs)

print tfidf_matrix.shape
print cosine_similarity(tfidf_matrix[0:1], tfidf_matrix)
cos_sim = 0 
angle_in_radians = math.acos(cos_sim)
print math.degrees(angle_in_radians)
