# -*- coding: utf-8 -*-

from sklearn.metrics.pairwise import cosine_similarity, pairwise_distances
from sklearn.feature_extraction.text import TfidfVectorizer

from alpes_core.term_frequency import words
from term_freq_Tese import words_tese

aux =[]
for tese in sorted(words_tese.items(), key=lambda x: x[1], reverse=True):
#     print tese[1]
    for posF in sorted(words.items(), key=lambda x: x[1], reverse=True):
#         print posF[1]   
        aux = (cosine_similarity(tese[1], posF[1]))
        
print aux