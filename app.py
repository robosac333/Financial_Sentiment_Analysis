from fastapi import FastAPI
import os
import requests
from dotenv import load_dotenv
from sentiment_analyzer import classify_sentiment, aggregate_sentiment

load_dotenv()
api_key = os.getenv('ALPHA_VANTAGE_API_KEY')

app = FastAPI()

def preprocess_text(text):
    return text.lower()

@app.get("/")
def home():
    """ Root endpoint """
    return {"message": "Welcome to the Sentiment Analysis API"}

@app.get("/sentiment")
def get_sentiment(ticker: str):
    """ Fetches news articles and returns aggregated sentiment analysis """
    url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={ticker}&apikey={api_key}'
    response = requests.get(url)
    data = response.json()

    sentiment_scores = []
    sentiment_labels = []

    if 'feed' in data:
        articles = data['feed']

        if not articles:
            return {"error": f"No news articles found for ticker: {ticker}"}

        processed_articles = []
        
        for article in articles:
            raw_title = article.get('title', 'No title available')
            raw_summary = article.get('summary', 'No summary available')

            clean_title = preprocess_text(raw_title)
            clean_summary = preprocess_text(raw_summary)

            combined_text = clean_title + ". " + clean_summary
            final_label, final_score = classify_sentiment(combined_text)

            sentiment_scores.append(final_score)
            sentiment_labels.append(final_label)

            processed_articles.append({
                "title": raw_title,
                "summary": raw_summary,
                "sentiment_label": final_label,
                "sentiment_score": round(final_score, 3)
            })

        final_sentiment, avg_score, most_common_label = aggregate_sentiment(sentiment_scores, sentiment_labels)

        return {
            "ticker": ticker,
            "final_sentiment": final_sentiment,
            "average_sentiment_score": round(avg_score, 3),
            "most_common_sentiment": most_common_label
        }
    else:
        return {"error": "No news data found from Alpha Vantage."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
