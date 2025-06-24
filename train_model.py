import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.metrics import accuracy_score
import joblib

# Load dataset
df = pd.read_csv('fake_or_real_news_sample.csv')

# Split data
X = df['text']
y = df['label']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# TF-IDF Vectorization
tfidf = TfidfVectorizer(stop_words='english', max_df=0.7)
X_train_vec = tfidf.fit_transform(X_train)
X_test_vec = tfidf.transform(X_test)

# Model training
model = PassiveAggressiveClassifier(max_iter=50)
model.fit(X_train_vec, y_train)

# Accuracy
y_pred = model.predict(X_test_vec)
score = accuracy_score(y_test, y_pred)
print(f'Accuracy: {round(score * 100, 2)}%')

# Save model and vectorizer
joblib.dump(model, 'model/fake_news_model.pkl')
joblib.dump(tfidf, 'model/tfidf_vectorizer.pkl')