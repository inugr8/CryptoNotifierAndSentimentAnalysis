# -*- coding: utf-8 -*-
"""CryptoNotifier.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1lhpTeaX7e_lg3H44vXK7VCZBFbfLPBG2
"""

from bs4 import BeautifulSoup
import requests
import time
import smtplib
import ssl
from email.mime.text import MIMEText as MT
from email.mime.multipart import MIMEMultipart as MM

import tweepy
from textblob import TextBlob
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

consumer_key ="your api key",
consumer_secret= "your api secret key",

 
# tweepy library to authenticate our API keys
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
api = tweepy.API(auth)
api = tweepy.API(
            auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True
       )

search_term='#bitcoin -filter:retweets'
tweets = tweepy.Cursor(api.search, q=search_term, lang='en',since='2018-11-01', tweet_mode='extended').items(2000)
all_twets = [tweet.full_text for tweet in tweets]

df = pd. DataFrame(all_twets, columns=['Tweets'])

def cleanTwt(twt):
  twt = re.sub('#Bitcoin', 'Bitcoin' , twt)
  twt = re.sub('#bitcoin', 'bitcoin' , twt)
  twt = re.sub('#BTC', 'Bitcoin' , twt)
  twt = re.sub('#[A-Za-z0-9]+', '' , twt)
  twt = re.sub('\\n', '' , twt)
  twt = re.sub('RT', '' , twt)
  twt = re.sub('https?:\/\/\S+', '' , twt)
  return twt

df['cleaned_tweets']=df['Tweets'].apply(cleanTwt)

def getSubjectivity(twt):
  return TextBlob(twt).sentiment.subjectivity
def getPolarity(twt):
  return TextBlob(twt).sentiment.polarity


df['Subjectivity']=df['cleaned_tweets'].apply(getSubjectivity)
df['Polarity']= df['cleaned_tweets'].apply(getPolarity)

def getSentiment(score):
  if score<0:
    return 'Negative'
  elif score==0:
    return 'Neutral'
  else:
    return 'Positive'


df['Sentiment'] = df['Polarity'].apply(getSentiment)


plt.figure(figsize=(8,6))

df['Sentiment'].value_counts().plot(kind='bar')
plt.title('Sentiment Analysis bar Plot')
plt.xlabel('Sentiment')
plt.ylabel('Number of Tweets')
plt.show()

def get_cryptoprice(coin):
  url = "https://www.google.com/search?q="+coin+"+price"
  HTML = requests.get(url)
  soup = BeautifulSoup(HTML.text,'html.parser')
  text = soup.find("div", attrs={'class': 'BNeawe iBp4i AP7Wnd'}).text
  return text

receiver = 'ishanukrishanaf9@gmail.com'
sender = 'crypto.news.at9@gmail.com'
sender_pass = '*****password!!!*****'

def send_email(sender, sender_pass , receiver , text_price):
  msg = MM()
  msg['Subect'] = "NEW  CRYPTO  PRICE  ALERT !!!!!"
  msg['From'] = sender
  msg['To'] = receiver
  HTML = """
          <html>
            <body>
              <h1>New Crypto Price Alert !!</h1>
              <h2>"""+text_price+"""</h2>
            </body>
          </html>"""
  MTObj = MT(HTML,"html")
  msg.attach(MTObj)
  SSL_context = ssl.create_default_context()
  server = smtplib.SMTP_SSL(host="smtp.gmail.com",port=465 , context = SSL_context)
  server.login(sender, sender_pass)
  server.sendmail(sender, receiver , msg.as_string())

def send_alert():
  last_price = -1
  while True:
    coin = 'bitcoin'
    price = get_cryptoprice(coin)
    if price != last_price  :
      print( coin.capitalize() + ' price : ', price)
      price_text= coin.capitalize()+' is '+price
      send_email(sender, sender_pass , receiver , price_text )
      last_price = price
      time.sleep(3)

send_alert()
