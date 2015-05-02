# -*- coding: utf-8 -*-

from sklearn.feature_extraction.text import CountVectorizer
from clusterArgFinal import sw_posFinal, sw_aux_tese, aux_usu
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics.pairwise import cosine_similarity, pairwise_distances

train_set =sw_aux_tese 
test_set = sw_posFinal
# print len(aux_usu)

grupo1 = []
grupo2 = []
grupo3 = []
grupo4 = []

vectorizer = CountVectorizer()
# print vectorizer

vectorizer.fit_transform(train_set)
# print vectorizer.vocabulary_

smatrix = vectorizer.transform(test_set)
# print smatrix

aux_smatrix =  smatrix.todense()
# print aux_smatrix

count_vectorizer = CountVectorizer()

count_vectorizer.fit_transform(train_set)
# print "Vocabulary:", 
count_vectorizer.vocabulary_

freq_term_matrix = count_vectorizer.transform(test_set)
# print freq_term_matrix.todense()

tfidf = TfidfTransformer(norm="l2")
tfidf.fit(freq_term_matrix)

# print "IDF:", tfidf.idf_

tf_idf_matrix = tfidf.transform(freq_term_matrix)
# print len(tf_idf_matrix.todense())

for i in range(0, len(test_set)):
    for j in range(i+1, len(test_set)):
#         print tf_idf_matrix[i], tf_idf_matrix[j]
        cos = cosine_similarity(tf_idf_matrix[i], tf_idf_matrix[j])
#         print "cos",cos
                        
        if cosine_similarity(tf_idf_matrix[i], tf_idf_matrix[j]) >= 0 and cosine_similarity(tf_idf_matrix[i], tf_idf_matrix[j]) <= 0.4: 
            if (aux_usu[i]+" com "+aux_usu[j]) not in grupo1 and (aux_usu[j]+" com "+aux_usu[i]) not in grupo1:
                grupo1.append(aux_usu[i]+" com "+aux_usu[j]+str(cos))
        elif cosine_similarity(tf_idf_matrix[i], tf_idf_matrix[j]) > 0.4 and cosine_similarity(tf_idf_matrix[i], tf_idf_matrix[j]) <= 0.7:
            if (aux_usu[i]+" com "+aux_usu[j]) not in grupo2 and (aux_usu[j]+" com "+aux_usu[i]) not in grupo2:
                grupo2.append(aux_usu[i]+" com "+aux_usu[j]+str(cos))
        elif cosine_similarity(tf_idf_matrix[i], tf_idf_matrix[j]) > 0.7 and cosine_similarity(tf_idf_matrix[i], tf_idf_matrix[j]) <= 1:
            if (aux_usu[i]+" com "+aux_usu[j]) not in grupo3 and (aux_usu[j]+" com "+aux_usu[i]) not in grupo3:
                grupo3.append(aux_usu[i]+" com "+aux_usu[j]+str(cos))
        else: 
            grupo4.append(aux_usu[i]+" com "+aux_usu[j]+str(cos))
#         print pairwise_distances(tf_idf_matrix[0:], tf_idf_matrix[0:], metric='euclidean')

print grupo1
print grupo2
print grupo3
print grupo4

# This was already calculated on the previous step, so we just use the value
# cos_sim = 0.52305744
# angle_in_radians = math.acos(cos_sim)
# print math.degrees(angle_in_radians)