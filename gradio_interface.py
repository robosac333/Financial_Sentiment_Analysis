import gradio as gr
import requests
import json

def analyze_sentiment(ticker):
    """
    Send request to FastAPI endpoint and format the response
    """
    try:
        response = requests.get(f"http://localhost:8000/api/v1/sentiment?ticker={ticker}")
        if response.status_code == 200:
            data = response.json()
            return f"""
                Ticker: {data['ticker']}
                Final Sentiment: {data['final_sentiment']}
                Average Sentiment Score: {data['average_sentiment_score']:.3f}
                Most Common Sentiment: {data['most_common_sentiment']}
            """
        else:
            return f"Error: {response.json().get('detail', 'Unknown error')}"
    except requests.RequestException as e:
        return f"Connection Error: Make sure the FastAPI server is running. Error: {str(e)}"

# Gradio interface
iface = gr.Interface(
    fn=analyze_sentiment,
    inputs=gr.Textbox(label="Enter Ticker Symbol (e.g., AAPL, MSFT, AMZN, NFLX)"),
    outputs=gr.Textbox(label="Sentiment Analysis Results"),
    title="Financial Sentiment Analysis",
    description="Enter a stock ticker symbol to analyze the sentiment of recent news articles."
)

if __name__ == "__main__":
    iface.launch()
