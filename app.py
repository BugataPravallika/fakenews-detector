from flask import Flask, render_template, request
from deep_translator import GoogleTranslator
import joblib
from fact_check import fact_check_news
from news_fetcher import get_live_headlines
import json
from datetime import datetime
import os

app = Flask(__name__)
model = joblib.load('model/fake_news_model.pkl')
vectorizer = joblib.load('model/tfidf_vectorizer.pkl')

@app.route('/')
def index():
    headlines = get_live_headlines()
    return render_template('index.html', headlines=headlines)

@app.route('/predict', methods=['POST'])
def predict():
    news = request.form['news']
    translated_news = GoogleTranslator(source='auto', target='en').translate(news)
    
    data = vectorizer.transform([translated_news])
    prediction = model.predict(data)[0]

    # ✅ Save history
    history = {
        'news': news,
        'translated': translated_news,
        'prediction': prediction,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    with open('history.json', 'a', encoding='utf-8') as f:
        f.write(json.dumps(history) + "\n")

    # ✅ Fact Check
    claim, rating = fact_check_news(translated_news)

    return render_template('result.html', prediction=prediction, news=news, translated=translated_news, claim=claim, rating=rating)


@app.route('/history')
def show_history():
    try:
        with open('history.json', 'r', encoding='utf-8') as f:
            lines = f.readlines()
            history_data = [json.loads(line.strip()) for line in lines]
    except FileNotFoundError:
        history_data = []

    return render_template('history.html', history=history_data)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
