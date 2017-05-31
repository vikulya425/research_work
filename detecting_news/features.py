import pandas as pd
import numpy as np
import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup
import redis
import requests
from readability.readability import Document
import re
import snowballstemmer as stem
from sklearn.feature_extraction.text import TfidfVectorizer
import shelve

def extract_features(db, i):

    first_features = []
    corpus= []

    for key in db:

        html_content = Document(key).summary()
        page_content = re.sub(r'\<[^>]*\>', '', html_content)
        stemmer = stem.stemmer('russian')
        stemmer = stemmer.stemWords(page_content.split())
        stem_content = ' '.join(stemmer)
        #if db[key]==1:
        corpus.append(stem_content)

        length = len(page_content)
        print("Starting ",i," str")
        soup = BeautifulSoup(key,'html.parser')
        title = soup.findAll('title')[0].string
        if (title.find("новост")!=-1):
            has_news_title = 1
        else:
            has_news_title = 0
        li_teg = len(soup.find_all('li'))
        ref = len(soup.find_all('a'))
        img = len(soup.find_all('img'))
        if (soup.find('link', type="application/rss+xml")):
            has_rss = 1
        else:
            has_rss = 0
        first_features.append([i,db[key], has_news_title, length, li_teg, ref, img, has_rss])
        i = i+1

    return first_features, corpus

if __name__ == "__main__":
    db = shelve.open('test.db')
    print(len(db.values()))
    i = 0
    (first, second) = extract_features(db,i)

    stop_words = 'а','бы','в','во','вот','для','до','если','же','за','и','из','или','к','ко','на','но','о','об','от','по','при','с','то','у','чтобы','это','да','нет','не'
    stemmer = stem.stemmer('russian')
    stemmer = stemmer.stemWords(stop_words)
    vec = TfidfVectorizer(max_features=40, stop_words=stemmer)
    fit = vec.fit_transform(second)

    train = open("train.csv", "w", newline="\n", encoding="utf-8")
    header1 = ['number', 'type', 'has_news_title', 'length', 'li', 'ref', 'img', 'has_rss']
    headers = np.hstack((header1, list(vec.vocabulary_)))
    features = np.hstack((first, fit.toarray()))
    csv.writer(train).writerow(headers)
    csv.writer(train).writerows(features)
    train.close()
