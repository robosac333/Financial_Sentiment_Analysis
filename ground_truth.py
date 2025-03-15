import requests
import os
from dotenv import load_dotenv
from typing import List, Dict, Any, Tuple
from collections import Counter

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv('ALPHA_VANTAGE_API_KEY')

def get_sentiment(ticker: str) -> Dict[str, Any]:
    """
    Get sentiment analysis for a given ticker.
    
    Args:
        ticker: Stock symbol to analyze
        
    Returns:
        Dictionary with aggregated sentiment analysis
    """
    url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={ticker}&apikey={api_key}'
    
    # Make API call to Alpha Vantage
    response = requests.get(url)
    data = response.json()
    
    if 'feed' not in data:
        print("Error: No feed data found in response")
        return {"error": "No data available"}
    
    # Extract ticker-specific sentiment from all articles
    sentiment_scores = []
    sentiment_labels = []
    
    for article in data['feed']:
        if 'ticker_sentiment' not in article:
            continue
        
        # Find the requested ticker in the article's ticker_sentiment list
        for ticker_data in article['ticker_sentiment']:
            if ticker_data['ticker'] == ticker:
                sentiment_scores.append(float(ticker_data['ticker_sentiment_score']))
                sentiment_labels.append(ticker_data['ticker_sentiment_label'])
                
                # Print details for this mention
                print(f"Article: {article['title']}")
                print(f"Relevance: {ticker_data['relevance_score']}")
                print(f"Sentiment Score: {ticker_data['ticker_sentiment_score']}")
                print(f"Sentiment Label: {ticker_data['ticker_sentiment_label']}")
                print("-----")
    
    # Aggregate the sentiment data
    if sentiment_scores:
        avg_score = sum(sentiment_scores) / len(sentiment_scores)
        most_common_label = Counter(sentiment_labels).most_common(1)[0][0]
        
        # Determine final sentiment based on thresholds from your data
        if avg_score >= 0.35:
            final_sentiment = "Bullish"
        elif 0.15 <= avg_score < 0.35:
            final_sentiment = "Somewhat-Bullish"
        elif -0.15 < avg_score < 0.15:
            final_sentiment = "Neutral"
        elif -0.35 < avg_score <= -0.15:
            final_sentiment = "Somewhat-Bearish"
        else:
            final_sentiment = "Bearish"
            
        # Print aggregated results
        print("\nAggregated Results:")
        print(f"Average Sentiment Score: {avg_score:.4f}")
        print(f"Most Common Label: {most_common_label}")
        print(f"Final Sentiment: {final_sentiment}")
        
        return {
            "ticker": ticker,
            "average_score": avg_score,
            "most_common_label": most_common_label,
            "final_sentiment": final_sentiment,
            "mentions_count": len(sentiment_scores)
        }
    else:
        print(f"No sentiment data found for ticker {ticker}")
        return {"error": f"No sentiment data found for {ticker}"}

if __name__ == "__main__":
    ticker = input("Enter ticker symbol: ")
    get_sentiment(ticker)