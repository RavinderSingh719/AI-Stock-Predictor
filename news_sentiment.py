from newsapi import NewsApiClient
from textblob import TextBlob

API_KEY = "e916472094bc48688b0ac8ca7d6e74ca"

newsapi = NewsApiClient(api_key=API_KEY)

def get_news_sentiment(company_name):

    articles = newsapi.get_everything(
        q=company_name,
        language="en",
        sort_by="publishedAt",
        page_size=10
    )

    sentiments = []

    for article in articles["articles"]:
        title = article["title"]
        analysis = TextBlob(title)
        sentiments.append(analysis.sentiment.polarity)

    if len(sentiments) == 0:
        return 0

    return sum(sentiments) / len(sentiments)
