# # -*- coding: utf-8 -*-

#lógia do algoritmo de tf-idf e cosine similarity
# from sklearn.feature_extraction.text import TfidfTransformer
# from sklearn.metrics.pairwise import cosine_similarity
# from sklearn.feature_extraction.text import CountVectorizer
# from nltk.cluster.util import cosine_distance
# 
# 
# 
# # train_set =sw_tese 
# # test_set = sw_posFinal
# test_set = st_posFinal
# train_set = st_tese
# # print len(aux_usu)
# 
# # for i in range(len(aux_usu)):
# #     print aux_usu[i],sw_posFinal[i]
# 
# grupo1 = []
# grupo2 = []
# grupo3 = []
# grupo4 = []
# nao_sim = []
# 
# vectorizer = CountVectorizer()
# # print vectorizer
# 
# vectorizer.fit_transform(train_set)
# # print vectorizer.vocabulary_
# 
# smatrix = vectorizer.transform(test_set)
# # print smatrix
# 
# aux_smatrix =  smatrix.todense()
# # print aux_smatrix
# 
# count_vectorizer = CountVectorizer()
# 
# count_vectorizer.fit_transform(train_set)
# # print "Vocabulary:", 
# count_vectorizer.vocabulary_
# 
# freq_term_matrix = count_vectorizer.transform(test_set)
# # print freq_term_matrix.todense()
# 
# tfidf = TfidfTransformer(norm="l2")
# tfidf.fit(freq_term_matrix)
# 
# # print "IDF:", tfidf.idf_
# 
# tf_idf_matrix = tfidf.transform(freq_term_matrix)
# # print len(tf_idf_matrix.todense())
# 
# #Tratamento das matrizes geradas pelo algoritmo de TF-IDF com a aplicação do cálculo do 
# #coseno entre os vetores - Cosine Similaridade
# for i in range(0, len(test_set)):
#     for j in range(i+1, len(test_set)):
#         cos = cosine_similarity(tf_idf_matrix[i], tf_idf_matrix[j])
#         
#         if cos >= 0.7 and cos <= 1 and \
#             (aux_usu[i]+" com "+aux_usu[j]) not in grupo1 and \
#             (aux_usu[i]+" com "+aux_usu[j]) not in grupo2 and \
#             (aux_usu[i]+" com "+aux_usu[j]) not in grupo3:
#             grupo1.append(aux_usu[i]+" com "+aux_usu[j]+ " - sim = " +str(cos))
#         elif cos >= 0.4 and cos < 0.7 and \
#             (aux_usu[i]+" com "+aux_usu[j]) not in grupo1 and \
#             (aux_usu[i]+" com "+aux_usu[j]) not in grupo2 and \
#             (aux_usu[i]+" com "+aux_usu[j]) not in grupo3:
#             grupo2.append(aux_usu[i]+" com "+aux_usu[j]+ " - sim = " +str(cos))
#         elif cos >= 0.2 and cos < 0.4 and \
#             (aux_usu[i]+" com "+aux_usu[j]) not in grupo1 and \
#             (aux_usu[i]+" com "+aux_usu[j]) not in grupo2 and \
#             (aux_usu[i]+" com "+aux_usu[j]) not in grupo3 :
#             grupo3.append(aux_usu[i]+" com "+aux_usu[j]+ " - sim = " +str(cos))
#         elif cos >= 0.1 and cos < 0.2 and \
#             (aux_usu[i]+" com "+aux_usu[j]) not in grupo1 and \
#             (aux_usu[i]+" com "+aux_usu[j]) not in grupo2 and \
#             (aux_usu[i]+" com "+aux_usu[j]) not in grupo3 :
#             grupo4.append(aux_usu[i]+" com "+aux_usu[j]+ " - sim = " +str(cos))
#         else:
#             nao_sim.append(aux_usu[i]+" com "+aux_usu[j]+ " - sim = " +str(cos))
# 
# 
# print len(grupo1)
# print "grup1:", grupo1, "\n"
# print len(grupo2)
# print "grup2:",grupo2, "\n"
# print len(grupo3)
# print "grup3:",grupo3, "\n"
# print len(grupo4)
# print "grup4:",grupo4, "\n"
# print len(nao_sim)
# print "nao_sim:",nao_sim, "\n"   