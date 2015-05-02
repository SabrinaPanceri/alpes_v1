from nltk.corpus import stopwords, floresta
from nltk.stem import RSLPStemmer
from nltk import RegexpTokenizer, re

stemmer = RSLPStemmer()

auxStopwords = stopwords.words('portuguese')
tokenizer = RegexpTokenizer("[\w’]+", flags=re.UNICODE)

def freq(word, tokens):
    return tokens.count(word)

vocabulary = []
docs = {}
all_tips = []