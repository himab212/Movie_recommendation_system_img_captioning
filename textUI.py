from flask import Flask
from flask import render_template, request
import json

app = Flask(__name__)
from nltk.stem import PorterStemmer
import re
from flask import Markup
from stop_words import get_stop_words

stop_words = get_stop_words('english')
p = PorterStemmer()


@app.route('/')
def hima():
    return render_template('text.html', content=output)


def rep(final, documentIdData):
    final2 = []
    for result in final:
        if (result.get('document_id') == documentIdData):
            final2.append(documentIdData)
            final2.append(result)
    return final2


@app.route('/result', methods=['POST', 'GET'])
def output():
    if request.method == 'POST':
        contentOfIDF = open('TFFIDF.txt', 'r').read()
        allContent = json.loads(contentOfIDF.lower())
        res = []
        try:
            text = request.form.get("textSearch").lower()
            partition = text.split(' ')

            for i in partition:
                if i not in stop_words:
                    if p.stem(i) in allContent:
                        for j in allContent[p.stem(i)]:
                            for k in partition:
                                if j.get("title").find(k) != -1:
                                    j.update(title=re.sub(k, Markup(
                                        "<mark style = \"background-color: pink;\">" + k + "</mark>"),
                                                          j.get('title')))



                            if (res == []):
                                res.append(j)
                            else:
                                redundant = rep(res, j.get("document_id"))
                                if(len(redundant)>0):
                                    j.update(tf=j.get("tf") + redundant[1].get("tf"))
                                    j.update(idf=j.get("idf") + redundant[1].get("idf"))
                                    j.update(tf_idf=j.get("tf_idf") + redundant[1].get("tf_idf"))
                                else:
                                    res.append(j)
                                    print(res)

        except:
            return render_template("except.html")



        ordered = sorted(res, key=lambda k: k['tf_idf'], reverse=True)
        print(ordered)
        return render_template("res.html", content=ordered)



if __name__ == '__main__':
    app.run()
