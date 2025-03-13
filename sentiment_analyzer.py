import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from collections import Counter

tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")

def classify_sentiment(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)

    probs = torch.softmax(outputs.logits, dim=-1).squeeze()
    negative_score = probs[0].item()
    neutral_score = probs[1].item()
    positive_score = probs[2].item()

    sentiment_score = positive_score - negative_score  

    if sentiment_score >= 0.5:
        sentiment_label = "Bullish"
    elif sentiment_score >= 0.2:
        sentiment_label = "Somewhat-Bullish"
    elif sentiment_score >= -0.2:
        sentiment_label = "Neutral"
    elif sentiment_score >= -0.5:
        sentiment_label = "Somewhat-Bearish"
    else:
        sentiment_label = "Bearish"

    return sentiment_label, sentiment_score

def aggregate_sentiment(sentiment_scores, sentiment_labels):
    if not sentiment_scores:
        return "No Sentiment Data", 0.0

    avg_score = sum(sentiment_scores) / len(sentiment_scores)
    most_common_label = Counter(sentiment_labels).most_common(1)[0][0]

    if avg_score >= 0.5:
        final_sentiment = "Bullish"
    elif avg_score >= 0.2:
        final_sentiment = "Somewhat-Bullish"
    elif avg_score >= -0.2:
        final_sentiment = "Neutral"
    elif avg_score >= -0.5:
        final_sentiment = "Somewhat-Bearish"
    else:
        final_sentiment = "Bearish"

    return final_sentiment, avg_score, most_common_label
