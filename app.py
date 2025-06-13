from flask import Flask, render_template, request
import pickle
from utils.text_from_url import extract_text_from_url
from langdetect import detect
from googletrans import Translator

app = Flask(__name__)

# Load ML model and vectorizer
model = pickle.load(open("model/model.pkl", "rb"))
vectorizer = pickle.load(open("model/vectorizer.pkl", "rb"))

translator = Translator()

@app.route('/', methods=['GET', 'POST'])
def home():
    result = None
    if request.method == 'POST':
        url = request.form['url']
        news_text = extract_text_from_url(url)
        language = detect(news_text)

        if language != 'en':
            translated = translator.translate(news_text, src=language, dest='en')
            translated_text = translated.text
        else:
            translated_text = news_text

        vec = vectorizer.transform([translated_text])
        prediction = model.predict(vec)[0]

        result = {
            'original': news_text,
            'translated': translated_text,
            'language': language,
            'classification': prediction
        }

    return render_template('index.html', result=result)
