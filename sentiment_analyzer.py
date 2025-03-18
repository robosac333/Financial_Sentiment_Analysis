import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from collections import Counter

# Loaded the FinBERT tokenizer and model from Hugging Face
tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")

def classify_sentiment(text):
    """
    Classified the sentiment of the input text using FinBERT.
    - Tokenized the input and converted it into tensors.
    - Obtained model outputs without computing gradients (in inference mode).
    - Applied softmax to obtain a probability distribution.
    - Calculated the sentiment score as half the difference between positive and negative scores.
    - Determined the sentiment label based on predefined thresholds.
    Returned a tuple containing the sentiment label and the sentiment score.
    """
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    probs = torch.softmax(outputs.logits, dim=-1).squeeze()
    
    negative = probs[0].item()
    neutral = probs[1].item()
    positive = probs[2].item()
    
    # Calculate a weighted sentiment score (-1 to 1 range)
    sentiment_score = positive - negative
    
    # More nuanced classification using both class probabilities and score
    if sentiment_score >= 0.5:
        sentiment_label = "Bullish"
    elif 0.2 <= sentiment_score < 0.5:
        sentiment_label = "Somewhat-Bullish"
    elif -0.2 <= sentiment_score < 0.2:
        sentiment_label = "Neutral"
    elif -0.5 <= sentiment_score < -0.2:
        sentiment_label = "Somewhat-Bearish"
    else:
        sentiment_label = "Bearish"
    return sentiment_label, sentiment_score

def aggregate_sentiment(sentiment_scores, sentiment_labels):
    """
    Aggregated multiple sentiment scores and labels by:
    - Computing the average sentiment score.
    - Determining the most common sentiment label using a counter.
    - Assigning a final sentiment label based on the average score.
    Returned a tuple containing the final sentiment label, the average score, and the most common label.
    """
    if not sentiment_scores:
        return "No Sentiment Data", 0.0, "No Data"
    
    avg_score = sum(sentiment_scores) / len(sentiment_scores)
    most_common_label = Counter(sentiment_labels).most_common(1)[0][0]
    
    # Use same thresholds as in classify_sentiment
    if avg_score >= 0.5:
        final_sentiment = "Bullish"
    elif 0.2 <= avg_score < 0.5:
        final_sentiment = "Somewhat-Bullish"
    elif -0.2 <= avg_score < 0.2:
        final_sentiment = "Neutral"
    elif -0.5 <= avg_score < -0.2:
        final_sentiment = "Somewhat-Bearish"
    else:
        final_sentiment = "Bearish"

    return final_sentiment, avg_score, most_common_label