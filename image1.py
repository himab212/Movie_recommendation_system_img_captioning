import os

from flask import Flask
from flask import render_template, request, send_from_directory
app = Flask(__name__)
from nltk.stem import PorterStemmer
ps = PorterStemmer()
from stop_words import get_stop_words
from nltk.tokenize import sent_tokenize, word_tokenize
import json

stop_words = get_stop_words('english')
@app.route('/')
def hima():
    return render_template('img.html')

@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory("Cons-3",filename="File"+filename+".jpg")

def checkDuplicateDocumentAndReturnIt(resultData,documentIdData):
    returnData=[]
    for result in resultData:
        if (result.get('document_id') == documentIdData):
            returnData.append(documentIdData)
            returnData.append(result)
    return returnData

@app.route('/imageCaptioning',methods = ['POST', 'GET'])
def classification():
    if request.method == 'POST':
        contentOfIDF = open('TF_IDF-img.txt', 'r').read()
        detailsOfAllData = json.loads(contentOfIDF.lower())
        result = []
        try:
            text = request.form.get("textSearch").lower()
            splitTextArray = text.split(' ')
            for i in splitTextArray:
                if i not in stop_words:
                    #print(ps.stem(i))
                    if ps.stem(i) in detailsOfAllData:
                        for j in detailsOfAllData[ps.stem(i)]:
                            if (result == []):
                                result.append(j)
                                print(result)
                            else:
                                duplicateData = checkDuplicateDocumentAndReturnIt(result, j.get('document_id'))
                                if (len(duplicateData) > 0):
                                    print("here")
                                    j.update(tf=j.get("tf") + duplicateData[1].get("tf"))
                                    j.update(idf=j.get("idf") + duplicateData[1].get("idf"))
                                    j.update(tf_idf=j.get("tf_idf") + duplicateData[1].get("tf_idf"))
                                else:
                                    result.append(j)

        except:
            print("exception is here")
            return render_template("error.html")
        sortedResult = sorted(result, key=lambda k: k['tf_idf'], reverse=True)
        return render_template("imgres.html", content=sortedResult)

if __name__ == '__main__':
    app.run(port='5001')
