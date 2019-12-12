
import pymysql
from stop_words import get_stop_words
import re
from flask import render_template, request
from flask import Flask
from collections import defaultdict
app = Flask(__name__)

@app.route('/')
def hima():
   return render_template('topclass.html')


@app.route('/classification',methods = ['POST', 'GET'])
def classify():
    if request.method == 'POST':

        text = request.form.get("textSearch").lower()
        db = pymysql.Connect(host='localhost',
                                 user='root',
                                 password='root1234',
                                 db='moviedb',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
        query = "SET sql_mode=(SELECT REPLACE(@@sql_mode, 'ONLY_FULL_GROUP_BY', ''));"
        with db.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(query)
        freqOfClass = "select category_id,title,genres, count(*) AS classFrequency from movies_metadata2 group by category_id;"
        with db.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(freqOfClass)
            movies = cursor.fetchall()
            #print(movies)

        allData = "SELECT id,tmdbid,imdb_id,title,overview,genres FROM movie"
        with db.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(allData)
            allcontent = cursor.fetchall()


        ProbabilityClassdic = []
        WordsCountOfClassdic = []

        for mv in movies:
            CP = {}
            WordsCount = {}
            counter = 0
            CP.update(genres=mv.get('genres'),
                                        classProbability=mv.get('classFrequency') / len(allcontent))
            ProbabilityClassdic.append(CP)
            for data in allcontent:

                if (mv.get('genres') == data.get('genres')):

                    if not ('title' == None):
                     temp = mv.get('title').split(' ')

                     counter = counter + len(temp)

            WordsCount.update(genres=mv.get('genres'), countOfwords=counter)
            WordsCountOfClassdic.append(WordsCount)


        def Frequency(mylist):
            freq = {}
            for item in mylist:
                if (item in freq):
                    freq[item] += 1
                else:
                    freq[item] = 1
            return freq

        Listcont = []
        stop_words = get_stop_words('english')


        for moviesdata in allcontent:

           if not (moviesdata.get('title') == None):
                 for word in moviesdata.get('title').split(' '):

                   if (word!= None):
                     word = re.sub("[^\w\s]", " ", word)

                 if word not in stop_words:
                    WordCategory = {}
                    WordCategory[word] = moviesdata.get("genres")
                    Listcont.append(WordCategory)

        WordCategDict = defaultdict(list)
        fWordCategDict = {}

        for d in Listcont:
            for key, value in d.items():
                WordCategDict[key].append(value)

        for h, m in WordCategDict.items():
            if not (h == ' '):
                wordFreqCount = Frequency(m)
                fWordCategDict[h] = wordFreqCount
        UniqueWords = len(fWordCategDict)

        onedict = {}
        ProbRes = {}
        probText = {}
        FullText = text.lower().split(' ')

        for i in FullText:

            try:

                for Word1 in fWordCategDict:
                    if (Word1.lower() == i):
                         onedict = fWordCategDict.get(Word1)

                for category in [o['genres'] for o in movies]:

                    for WordCounts in WordsCountOfClassdic:
                        WordCount1 = 0

                        if (WordCounts.get('genres') == category):
                            WordCount1 = WordCounts.get('genres')
                            if not (category in onedict.keys()):
                                cFrequency = 0
                            else:
                                cFrequency = onedict.get(category)
                    proCA = (cFrequency + 1) / (WordCount1 + UniqueWords)
                    categoryDict = {category: proCA}
                    ProbRes.update(categoryDict)
                    probText[i] = ProbRes
                    print(probText)
            except:
                print("fail")


        chooseCa = {}
        for category in movies:
            for probOfClass in ProbabilityClassdic:

                if (category.get('genres') == probOfClass.get('genres')):
                    prochooseCategory = probOfClass.get('classProbability')
                    chooseCa[probOfClass.get('genres')] = prochooseCategory
        print(chooseCa)


        return render_template("resy.html", classificationResult=chooseCa)



if __name__ == '__main__':
    app.run(port='5002')