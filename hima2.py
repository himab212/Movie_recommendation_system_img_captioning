import json
import math
import numpy as np
import pymysql

from flask import Flask, render_template, request, jsonify
from stop_words import get_stop_words

import nltk
nltk.download('punkt')

from nltk.stem import PorterStemmer
ps = PorterStemmer()

from nltk.tokenize import sent_tokenize, word_tokenize




conn = pymysql.Connect(host='localhost',user='root',password='root1234',db='moviedb',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)

query = "SELECT id,url,caption FROM image2"
with conn.cursor(pymysql.cursors.DictCursor) as cursor:
    cursor.execute(query)
    movies = cursor.fetchall()


tfArray = []
i=0
idfArray = []
stop_words = get_stop_words('english')
recordTF_IDF_Dictionary = {}
recordTFDictionary = {}
recordIDF_Dictionary = {}

def stemSentence(sentence):
    token_words = word_tokenize(sentence)

    stem_sentence = []
    for word in token_words:
        stem_sentence.append(ps.stem(word))
        stem_sentence.append(" ")
    return "".join(stem_sentence)

def calculateIDF(word, dataMovies, recordIDF_Dictionary, tf, docId,title):
    ''', channelTitle, views,likes, dislikes):'''
    wordCountIdf = 0
    for dataMovie in dataMovies:
        titleText= dataMovie["caption"]
        titleText = stemSentence(titleText)
        wordCountIdf += titleText.count(word)
    idf = math.log10(len(movies)/wordCountIdf)
    docIDFdic = {'document_id':docId, 'idf':idf}
    docTF_IDFDict = {'document_id':docId, 'tf_idf':tf*idf, 'tf':tf, 'idf':idf, 'title':title}
    if word not in recordIDF_Dictionary:
        word_IDF_Arr = []
        word_IDF_Arr.append(docIDFdic)
        recordIDF_Dictionary.update({word: word_IDF_Arr})
        word_TF_IDF_Arr = []
        word_TF_IDF_Arr.append(docTF_IDFDict)
        recordTF_IDF_Dictionary.update({word: word_TF_IDF_Arr})
    else:
        recordIDF_Dictionary.get(word).append(docIDFdic)
        recordTF_IDF_Dictionary.get(word).append(docTF_IDFDict)
    print(recordTF_IDF_Dictionary)
    return recordIDF_Dictionary

for data in movies:
   text = data["caption"]
   caption = data["caption"]
   docId = data["id"]
   text = stemSentence(text)
   list_str = text.split()
   wordslist = list(set(list_str))
   tfDictionary = ({})
   idfDictionary = ({})


   wordCountIdf = 0

   for word in wordslist:
       word = ps.stem(word)
       if word not in stop_words:
        wordCount = text.count(word)
        totalWordCount = len(text)
        tf = wordCount / totalWordCount
        docTfdic = {'document_id' : docId, 'tf': tf}
        if word not in recordTFDictionary:
            s=[]
            s.append(docTfdic)
            recordTFDictionary.update({word:s})
        else:
            recordTFDictionary.get(word).append(docTfdic)
        recordIDF_Dictionary = calculateIDF(word, movies, recordIDF_Dictionary,tf,docId,caption)
        wordCountIdf += wordCount
       else:
           print("stop word" + word)



with open('TF-img1.txt', 'w') as json_file:
  json.dump(recordTFDictionary, json_file)
with open('IDF-img1.txt', 'w') as json_file:
      json.dump(recordIDF_Dictionary, json_file)
with open('TF_IDF-imgg1.txt', 'w') as json_file:
  json.dump(recordTF_IDF_Dictionary, json_file)


conn.close()
app = Flask(__name__)
@app.route('/textSearch', methods=['POST'])
def textSearch():
    if __name__ == '__main__':
        app.run()