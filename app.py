# Imported necessary libraries and modules
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import os
import httpx
from dotenv import load_dotenv

from preprocess import preprocess_text
from sentiment_analyzer import classify_sentiment, aggregate_sentiment

# Loaded environment variables from the .env file (e.g., the API key)
load_dotenv()
api_key = os.getenv('ALPHA_VANTAGE_API_KEY')


# Initialized the FastAPI application with metadata
app = FastAPI(
    title="Financial Sentiment Analysis API",
    description="API for analyzing financial news sentiment using FinBERT.",
    version="1.0.0"
)

# Defined the response model using Pydantic (this model was used to structure API responses)
class SentimentResponse(BaseModel):
    ticker: str = Field(..., example="AAPL")
    final_sentiment: str = Field(..., example="Bullish")
    average_sentiment_score: float = Field(..., example=0.345)
    most_common_sentiment: str = Field(..., example="Bullish")


@app.get("/", tags=["General"])
def home():
    """
    Provided a basic message at the root endpoint.
    """
    return {"message": "Welcome to the Financial Sentiment Analysis API"}

@app.get("/api/v1/sentiment", response_model=SentimentResponse, tags=["Sentiment Analysis"])
async def get_sentiment(ticker: str):
    """
    Processed a request for sentiment analysis for a given ticker.
    - Built the API URL for Alpha Vantage using the provided ticker.
    - Made an asynchronous HTTP request to Alpha Vantage.
    - Checked for API rate limits or error messages in the response.
    - Preprocessed the title and summary for each news article.
    - Classified sentiment using FinBERT.
    - Aggregated the sentiment scores and labels.
    Returned the aggregated sentiment analysis using the defined response model.
    """
    url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={ticker}&apikey={api_key}'
    
    # Made an asynchronous API call to Alpha Vantage
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
        response.raise_for_status()
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Error fetching news data: {e}")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=response.status_code, detail=f"HTTP error: {e}")

    data = response.json()
    
    # Checked for rate limit or error messages from Alpha Vantage
    if "Note" in data:
        raise HTTPException(status_code=429, detail=f"API rate limit reached: {data['Note']}")
    if "Error Message" in data:
        raise HTTPException(status_code=400, detail=f"API error: {data['Error Message']}")
    
    sentiment_scores = []
    sentiment_labels = []

    # Processed the news articles if available
    if 'feed' in data:
        articles = data['feed']
        if not articles:
            raise HTTPException(status_code=404, detail=f"No news articles found for ticker: {ticker}")
        
        # Iterated through each article
        for article in articles:
            raw_title = article.get('title', 'No title available')
            raw_summary = article.get('summary', 'No summary available')
            
            # Preprocessed the title and summary
            clean_title = preprocess_text(raw_title)
            clean_summary = preprocess_text(raw_summary)
            
            # Combined the preprocessed title and summary
            combined_text = f"{clean_title}. {clean_summary}"
            
            # Classified sentiment using FinBERT
            final_label, final_score = classify_sentiment(combined_text)
            sentiment_scores.append(final_score)
            sentiment_labels.append(final_label)

        # Aggregated the sentiment scores and labels to determine the final result
        final_sentiment, avg_score, most_common_label = aggregate_sentiment(sentiment_scores, sentiment_labels)

        return SentimentResponse(
            ticker=ticker,
            final_sentiment=final_sentiment,
            average_sentiment_score=round(avg_score, 3),
            most_common_sentiment=most_common_label
        )
    else:
        # Raised an error if no news data was found from Alpha Vantage
        raise HTTPException(status_code=404, detail="No news data found from Alpha Vantage.")

# Ran the FastAPI application using Uvicorn when this module was executed directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=5000, reload=True)
