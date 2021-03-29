from flask import Flask, render_template,url_for,request
import wikipedia
import spacy
from spacy import displacy
from spacy.lang.en import English
from flaskext.markdown import Markdown
import random

nlp = spacy.load("en_core_web_sm")

#init app
app = Flask(__name__)
Markdown(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/extract', methods=['GET', 'POST'])
def extract():
    if request.method == 'POST':
        data = request.form['searched']        
        try:
            rawText = wikipedia.summary(data)
        except wikipedia.DisambiguationError as e:
            s = random.choice(e.options)
            rawText = wikipedia.summary(s,sentences = 10)
        docx = nlp(rawText)
        html = displacy.render(docx,style='ent')
        result = html
    return render_template('results.html',rawText=rawText,result=result)

if __name__=='__main__':
    app.run(debug=True, port=8000)