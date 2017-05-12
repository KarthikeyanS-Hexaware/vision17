# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 15:55:37 2017

@author: 30216
"""
import sys
sys.path.append("C:\Python27\Lib\site-packages")
import re
import numpy as np
from textblob import TextBlob
import pandas as pd

class TwitterSentiment(object):
    
    def clean_tweet(self, tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
    
    def get_tweet_sentiment(self, tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'
    
    def get_tweets(self,query):
        
        # empty list to store parsed tweets        
        tweets=[]
        #call the query and extract the tweets
        #tweet_text = query['twt_text']
        tweet_text = query['text']
        #parsing tweets one by one
        for tweetCnt in range(0,len(tweet_text)):
            # empty dictionary to store required params of a tweet
            parsed_tweet = {}
            # saving text of tweet
            parsed_tweet['text'] = tweet_text[tweetCnt]
            # saving sentiment of tweet
            parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet_text[tweetCnt])
            #appending the tweets
            tweets.append(parsed_tweet)
        #return parsed tweets
        return tweets
        
def main():
    
    # creating object of TwitterClient Class
    api = TwitterSentiment()
    #importing the extracted data for recent tweets
    twitter_data = pd.read_csv("D:\\POC\Vision 2017\\Twitter data\\For older tweets\\GetOldTweets-python-master\\output_got.csv")
    #importing the extracted data for older tweets
    #twitter_data = pd.read_csv("D:\\POC\\Vision 2017\\Twitter data\\recent tweets\\brexit.csv")
    #removing the empty tweets
    #twitter_data = twitter_data[pd.notnull(twitter_data['twt_text'])]
    twitter_data = twitter_data[pd.notnull(twitter_data['text'])]
    #reseting the index
    twitter_data = twitter_data.reset_index(drop=True)
    # calling function to get tweets
    tweets = api.get_tweets(query = twitter_data)
    # picking positive tweets from tweets
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    # percentage of positive tweets
    print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets)))
    # picking negative tweets from tweets
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    # percentage of negative tweets
    print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets)))
    # picking neutral tweets from tweets
    neutraltweets = [tweet for tweet in tweets if tweet['sentiment'] == 'neutral']    
    # percentage of neutral tweets    
    print("Neutral tweets percentage: {} % \
        ".format(100*(len(tweets) - len(ntweets) - len(ptweets))/len(tweets)))
        
    # printing first 5 positive tweets
    print("\n\nPositive tweets:")
    for tweet in ptweets[:10]:
        print(tweet['text'])
 
    # printing first 5 negative tweets
    print("\n\nNegative tweets:")
    for tweet in ntweets[:10]:
        print(tweet['text'])
        
    # printing first 5 neutral tweets
    print("\n\nNeutral tweets:")
    for tweet in neutraltweets[:10]:
        print(tweet['text'])
 
if __name__ == "__main__":
    # calling main function
    main()