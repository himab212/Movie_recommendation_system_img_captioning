import json
import math
from flask import Flask
from stop_words import get_stop_words
import pymysql

conn = pymysql.Connect(host='localhost',user='root',password='root1234',db='moviedb',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)

query = "SELECT id,genres,rating_userid,title,overview,tmdbid,imdb_id,poster_path FROM movie"
with conn.cursor(pymysql.cursors.DictCursor) as cursor:
    cursor.execute(query)
    movies = cursor.fetchall()


tfArray = []
i=0
idfArray = []
stop_words = get_stop_words('english')
tf_file = open("TF1.txt","w+")
recordTF_IDF_Dictionary = {}
recordTFDictionary = {}
recordIDF_Dictionary = {}



def calculateIDF(word, dataMovies, recordIDF_Dictionary, tf, id,title,  tmdbid,imdbid):
    wordCountIdf = 0
    idf=0
    for dataVideo in dataMovies:
        titleText = dataVideo["title"]
        if(titleText!= None):
         wordCountIdf += titleText.count(word)
    if(wordCountIdf!=0):
     idf = math.log(len(movies) / wordCountIdf)
    docIDFdic = {'doc_id': id, 'idf': idf}
    docTF_IDFDict = {'doc_id': id, 'tf_idf': tf * idf, 'tf': tf, 'idf': idf, 'title': title, 'tmdbid' : tmdbid, 'imdb_id' :  imdbid}

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
    return recordIDF_Dictionary

for data in movies:
   text = data["title"]
   id =data["id"]
   title = data["title"]
   tmdbid= data["tmdbid"]
   imdbid = data["imdb_id"]
   if(text!=None):
    list_str = text.split()
    wordslist = list(set(list_str))
    tfDictionary = ({})
    idfDictionary = ({})


   wordCountIdf = 0

   for word in wordslist:
       if word not in stop_words:
        if(text!=None):
         wordCount = text.count(word)
         if (len(text) != 0):
          totalWordCount = len(text)
         tf = wordCount / totalWordCount
        docTfdic = {'doc_id' : id, 'tf': tf}
        if word not in recordTFDictionary:
            s=[]
            s.append(docTfdic)
            recordTFDictionary.update({word:s})
        else:
            recordTFDictionary.get(word).append(docTfdic)
        recordIDF_Dictionary = calculateIDF(word, movies, recordIDF_Dictionary,tf,id, title,  tmdbid,imdbid)
        wordCountIdf += wordCount

       else:
           print("stop word " + word)

with open('Tf.txt', 'w') as json_file:
  json.dump(recordTFDictionary, json_file)
with open('IIddff.txt', 'w') as json_file:
      json.dump(recordIDF_Dictionary, json_file)
with open('TFFIDF.txt', 'w') as json_file:
  json.dump(recordTF_IDF_Dictionary, json_file)


conn.close()
app = Flask(__name__)
@app.route('/textSearch', methods=['POST'])
def textSearch():
    if __name__ == '__main__':
        app.run()