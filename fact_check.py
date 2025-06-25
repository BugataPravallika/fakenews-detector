# factcheck.py
import requests

API_KEY = "AIzaSyCY3S9fz_gw2BlCpq23vqYeyZX-IYewVAE"

def fact_check_news(query):
    url = "https://factchecktools.googleapis.com/v1alpha1/claims:search"
    params = {
        "query": query,
        "key": API_KEY,
        "languageCode": "en"
    }

    response = requests.get(url, params=params)
    data = response.json()

    if "claims" in data:
        claim = data["claims"][0]
        text = claim.get("text", "No claim text found")
        rating = claim["claimReview"][0].get("textualRating", "No rating found")
        return text, rating
    else:
        return "No fact check found", "Unknown"
