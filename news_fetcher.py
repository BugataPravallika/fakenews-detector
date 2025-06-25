import requests

API_KEY = '0d8a5d61ad5c46058498e0fcfc40a546'
NEWS_API_URL = f"https://newsapi.org/v2/top-headlines?country=in&language=en&pageSize=10&apiKey={API_KEY}"

def get_live_headlines():
    try:
        response = requests.get(NEWS_API_URL)
        response.raise_for_status()
        data = response.json()
        articles = data.get('articles', [])
        headlines = [{"title": article['title'], "description": article.get("description", "")} for article in articles]
        return headlines
    except Exception as e:
        print("Error fetching news:", e)
        return []
