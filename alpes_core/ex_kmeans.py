import collections
 
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster.k_means_ import MiniBatchKMeans

def cluster_texts(texts, clusters):
    """ Transform texts to Tf-Idf coordinates and cluster texts using K-Means """
#     vectorizer = TfidfVectorizer(tokenizer=process_text,
#                                  stop_words=stopwords.words('portuguese'),
#                                  max_df=0.5,
#                                  min_df=0.1,
#                                  lowercase=True)
    vectorizer = TfidfVectorizer(max_df=0.6,
                                 min_df=0.3)
 
    tfidf_model = vectorizer.fit_transform(texts)
#     km_model = MiniBatchKMeans(n_clusters=clusters)    
    km_model = KMeans(n_clusters=clusters)
    km_model.fit_transform(tfidf_model)
    clustering = collections.defaultdict(list)
 
    for idx, label in enumerate(km_model.labels_):
        clustering[label].append(idx)
 
    return clustering