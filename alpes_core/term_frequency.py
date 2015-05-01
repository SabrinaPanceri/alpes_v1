from nltk.corpus import stopwords
from nltk import RegexpTokenizer, re

stopwords = stopwords.words('portuguese')
tokenizer = RegexpTokenizer("[\w']+", flags=re.UNICODE)

def freq(word, tokens):
    return tokens.count(word)


#Compute the frequency for each term.
vocabulary = []
docs = {}
all_tips = []


for tip in (venue.tips()):
    tokens = tokenizer.tokenize(tip.text)

    bi_tokens = bigrams(tokens)
    tri_tokens = trigrams(tokens)
    tokens = [token.lower() for token in tokens if len(token) > 2]
    tokens = [token for token in tokens if token not in stopwords]

    bi_tokens = [' '.join(token).lower() for token in bi_tokens]
    bi_tokens = [token for token in bi_tokens if token not in stopwords]

    tri_tokens = [' '.join(token).lower() for token in tri_tokens]
    tri_tokens = [token for token in tri_tokens if token not in stopwords]

    final_tokens = []
    final_tokens.extend(tokens)
    final_tokens.extend(bi_tokens)
    final_tokens.extend(tri_tokens)
    docs[tip.text] = {'freq': {}}

    for token in final_tokens:
        docs[tip.text]['freq'][token] = freq(token, final_tokens)

print docs
