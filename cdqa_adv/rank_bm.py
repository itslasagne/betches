from nltk import pos_tag
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import requests
# from googlesearch import search
import bs4
import numpy as np
import re
import os
from tika import parser
import pandas as pd

#download nltk-stopwords
import nltk
nltk.download("stopwords")
nltk.download('punkt')
nltk.download('wordnet')

#search engine
from rank_bm25 import BM25Okapi
from rank_bm25 import BM25Plus
from rank_bm25 import BM25L


'''====================================================
            rank_bm25 model(search engine)
======================================================= '''

stop_words = list(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()


class rank_bm25:

    def __init__(self, query, documents,para_threshold=2):
        self.query = query
        self.documents = documents
        self.para_threshold = para_threshold


    def word_token(self, tokens, lemma=False):
        tokens = str(tokens)
        tokens = re.sub(
            r"([\w].)([\~\!\@\#\$\%\^\&\*\(\)\-\+\[\]\{\}\/\"\'\:\;])([\s\w].)", "\\1 \\2 \\3", tokens)
        tokens = re.sub(r"\s+", " ", tokens)
        if lemma:
            return " ".join([lemmatizer.lemmatize(token, 'v') for token in word_tokenize(tokens.lower()) if token not in stop_words and token.isalpha()])
        else:
            return " ".join([token for token in word_tokenize(tokens.lower()) if token not in stop_words and token.isalpha()])


    def get_similarity(self):
        docs = self.query + self.documents
        docs = [self.word_token(d, lemma=True) for d in docs]
        tokenized_corpus = [doc.split(' ') for doc in docs]
        bm25 = BM25Okapi(tokenized_corpus[1:])
        bm25plus = BM25Plus(tokenized_corpus[1:])
        bm25L = BM25L(tokenized_corpus[1:])

        self.query = tokenized_corpus[0]
        bm25_scores = bm25.get_scores(self.query)
        bm25plus_scores = bm25plus.get_scores(self.query)
        bm25L_scores = bm25L.get_scores(self.query)

        bm25_scores = [(i, v) for i, v in enumerate(bm25_scores)]
        bm25plus_scores = [(i, v) for i, v in enumerate(bm25plus_scores)]
        bm25L_scores = [(i, v) for i, v in enumerate(bm25L_scores)]

        bm25_scores.sort(key=lambda x: x[1], reverse=True)
        bm25plus_scores.sort(key=lambda x: x[1], reverse=True)
        bm25L_scores.sort(key=lambda x: x[1], reverse=True)

        return bm25_scores, bm25plus_scores, bm25L_scores


    def select_context(self):

        bm_1, _, _ = self.get_similarity()
        bm_1 = np.array(bm_1)
        bm_1_idx = bm_1[bm_1[:, 1] > 1][:self.para_threshold, 0]
        bm_1_idx = np.array(bm_1_idx, dtype=int)
        if bm_1_idx.size == 0:
          bm_1_idx=np.array([0])

        return ' '.join(self.documents[i] for i in sorted(bm_1_idx)), ','.join( str(i+1) for i in bm_1_idx)
