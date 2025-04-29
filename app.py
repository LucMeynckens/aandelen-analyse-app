import streamlit as st
import yfinance as yf
import requests
from bs4 import BeautifulSoup
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd

st.set_page_config(page_title="Aandelen Dashboard", layout="wide")
st.title("?? Aandelenanalyse met Koers & Sentiment")

ticker = st.text_input("Voer een tickersymbool in (bv. AAPL, MSFT, TSLA)", "AAPL")

# Koersdata ophalen via yfinance
data = yf.Ticker(ticker)
hist = data.history(period="1y")

col1, col2 = st.columns(2)
col1.metric("Laatste slotkoers", f"${hist['Close'][-1]:.2f}")
col2.metric("52W Hoog", f"${hist['High'].max():.2f}")

st.line_chart(hist["Close"])

# Nieuws headlines ophalen van Yahoo Finance
st.subheader("?? Nieuws & Sentiment")

url = f"https://finance.yahoo.com/quote/{ticker}/news"
headers = {'User-Agent': 'Mozilla/5.0'}
html = requests.get(url, headers=headers).text
soup = BeautifulSoup(html, 'html.parser')
headlines = [tag.text for tag in soup.find_all('h3')][:5]

analyzer = SentimentIntensityAnalyzer()
scores = []

for h in headlines:
    score = analyzer.polarity_scores(h)['compound']
    scores.append(score)
    st.write(f"• {h} ? **Sentiment:** `{score:.2f}`")

# Gemiddeld sentiment + advies
avg_sentiment = sum(scores) / len(scores) if scores else 0
st.write(f"**Gemiddeld sentiment:** `{avg_sentiment:.2f}`")

if avg_sentiment > 0.2:
    st.success("Positief sentiment ? ?? Koopsignaal")
elif avg_sentiment < -0.2:
    st.error("Negatief sentiment ? ?? Verkoopsignaal")
else:
    st.warning("Neutraal sentiment ? ?? Afwachten")

