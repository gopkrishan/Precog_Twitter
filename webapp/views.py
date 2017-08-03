# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from .forms import NameForm

import tweepy
import json
import re
import matplotlib.pyplot as plt
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from pymongo import MongoClient
from textblob import TextBlob
from wordcloud import WordCloud

# Create your views here.
#Twitter Keys for authentication
ckey='ayYkm6ZqsbGA0m8pxyQ23bbG1'
csecret='syHndXDHhjqs3amqT1hyXThbe7fZpNDsH6MrVxKoxoz7cmFZQH'
atoken='892379507994144768-138GMhkV5AfR3Vj6xVhWRMvXUeSIQ3k'
asecret='vKwtydYtu0BazaMtGstWsevRC1jJcQ1Smcxi9QDAv3s7J'

auth=OAuthHandler(ckey,csecret)
auth.set_access_token(atoken,asecret)

#Mongodb to use as localhost
client=MongoClient('localhost:27017')
db=client.Twitter

tweets=[] #stores all the tweets in json format
ind=0
collection=db.TwitterData

def storeinmongo(): #TO Store Data
	global tweets
	for tweet in tweets:
		print tweet
		collection.insert(tweet)
	print len(tweets)

def get_tweet(text): #For Extraction of Tweets of particular hashtag
	api=tweepy.API(auth)
	Tweets = tweepy.Cursor(api.search, q=text).items(200)
	for t in Tweets:
	    tweets.append(t._json)
	print len(tweets)
	storeinmongo()

def drawplot(): #Function for loacation
	itera=collection.find()
	locn=[]
	counter=0
	places=[]
	for t in itera:
		s=t['user']['location']
		locn=s.split(',')
		if(len(locn)>=2):
			loc=locn[len(locn)-1]
			x=loc.lower()
			if(x not in places):
				places.append(x)
	finallist=[[] for i in range(len(places))]
	for i in range(len(places)):
		finallist[i].append(places[i])
		finallist[i].append(100)
	return finallist


def tophashtags():
	itera=collection.find()
	hashtags={}
	hashes=[]
	for t in itera:
		temp=t['entities']['hashtags']
		if(temp):
			for i in range(len(temp)):
				s=temp[i]['text']
				if(s not in hashes):
					hashes.append(s)
					hashtags[s]=1
				else:
					hashtags[s]=hashtags[s]+1
	hashtags_r = sorted(hashtags, key=hashtags.get, reverse=True)
	count=0
	for i in hashtags_r:
		if(count>10):
			break
		else:
			print i,hashtags[i]
		count=count+1
	wordcloud = WordCloud()
	wordcloud.generate_from_frequencies(frequencies=hashtags)
	image = wordcloud.to_image()
	image.save('./webapp/static/project_pre/images/WordCloud.png')


def text_images():
	itera=collection.find()
	types=['Text','Text+Images']
	count=[0,0]
	counter=0
	for t in itera:
		if('media' in t['entities'] and t['text']):
			count[1]=count[1]+1
			counter=counter+1
		else:
			count[0]=count[0]+1
	finallist=[[types[0],count[0]],[types[1],count[1]]]

	return finallist

def tweet_retweet():
	itera=collection.find()
	types=['Tweets','Retweets']
	count=[0,0]
	for t in itera:
		if('retweeted_status' in t):
			count[1]=count[1]+1
		else:
			count[0]=count[0]+1
	finallist=[[types[0],count[0]],[types[1],count[1]]]
	return finallist


def clean_tweet(s):
	return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ",s).split())

def get_sentiment(text):
	analysis = TextBlob(clean_tweet(text))
	if analysis.sentiment.polarity > 0.0:
		return 'positive'
	elif analysis.sentiment.polarity == 0.0:
		return 'neutral'
	else:
		return 'negative'

def get_popularity():
	itera=collection.find()
	tweet=[]
	count=0
	for t in itera:
		s=t['user']['location']
		temp=s.split(',')
		if('New Delhi' or 'Delhi' or 'delhi' or 'new delhi' in temp):
			count=count+1
            #further code to give some count on popualrity
			query_tweet={}
			query_tweet['text']=t['text']
			query_tweet['sentiment']=get_sentiment(t['text'])
			if(t['retweet_count'] > 0):
				if(t['text'] not in tweet):
					tweet.append(query_tweet)
			else:
				tweet.append(query_tweet)
	positive_tweets=[]
	negative_tweets=[]
	neutral_tweets=[]
	for i in range(len(tweet)):
		print i,type(tweet[i]['sentiment'])
		if(tweet[i]['sentiment']=="positive"):
			positive_tweets.append(tweet[i]['text'])
		elif(tweet[i]['sentiment']=="negative"):
			negative_tweets.append(tweet[i]['text'])
		else:
			neutral_tweets.append(tweet[i]['text'])

	count=[len(positive_tweets)*100/len(tweet),len(negative_tweets)*100/len(tweet),len(neutral_tweets)*100/len(tweet)]
	types=['positive','negative','neutral']
	finallist=[[types[0],count[0]],[types[1],count[1]],[types[2],count[2]]]
	return finallist

def get_fav_count():
	itera=collection.find()
	fav_count_tweets={} #Dictionary to store the tweets with the fav count
	total=0
	fav_count=0
	for t in itera:
		total=total+t['user']['favourites_count']
		if('retweeted_status' not in t):
			fav_count_tweets[t['id']]=t['user']['favourites_count']
			fav_count=fav_count+t['user']['favourites_count']
	print fav_count,total
	explode=[0,0]
	count=[fav_count,total-fav_count]
	types=['Original','Retweeted']
	finallist=[[types[0],count[0]],[types[1],count[1]]]
	return finallist

class HomePageView(TemplateView):

	def get(self,request,**kwargs):
		form=NameForm()
		return render(request,'index.html',{'form':form})

	def post(self,request):
		form=NameForm(request.POST)
		if form.is_valid():
			text=form.cleaned_data['hashtag']
		else:
			form=NameForm()

		#args={'form':form,'text':text}

		print(text)
		get_tweet(text) #To extract tweet from Twitter with the particular hashtag

		location=drawplot()     #Plots the tweets according to the location

		tophashtags() #Generates a Word Cloud of tophashes

		teimg=json.dumps(text_images()) #Distribution of the tweet wheather it is text or text+image

		twertw=json.dumps(tweet_retweet()) #Distribution of the tweets if its original or retweeted_status

		popul=json.dumps(get_popularity()) #Generates the positivity,negativity and distribution of the tweets in Delhi

		favour=json.dumps(get_fav_count())

		return render(request,'display.html',{'Location_Tweet':location,'text_images': teimg , 'tweet_retweet':twertw ,'popularity':popul ,'favcount':favour})
