from gensim import corpora, models, similarities
from nltk.corpus import stopwords
import re

def cleanword(word):
    return re.sub(r'\W+', '', word).strip()

def lsi_app(documents):

    # remove common words and tokenize
    stoplist = stopwords.words('portuguese')
    stoplist.append('')
    texts = [[cleanword(word) for word in document.lower().split() if cleanword(word) not in stoplist]
             for document in documents]
    
#     print "texts", texts
    
    # remove words that appear only once
    all_tokens = sum(texts, [])
    
    tokens_once = set(word for word in set(all_tokens) if all_tokens.count(word) == 1)

    texts = [[word for word in text if word not in tokens_once] for text in texts]
    
    dictionary = corpora.Dictionary(texts)
#     print "dictionary", dictionary
    corp = [dictionary.doc2bow(text) for text in texts]
#     print corp

    # extract 400 LSI topics; use the default one-pass algorithm
    lsi = models.lsimodel.LsiModel(corpus=corp, id2word=dictionary, num_topics=400)
    # print the most contributing words (both positively and negatively) for each of the first ten topics

    index = similarities.MatrixSimilarity(corp, num_features=len(dictionary))
    
    print str(index)
    
    return index