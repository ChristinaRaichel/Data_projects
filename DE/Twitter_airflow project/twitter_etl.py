import pandas as pd 
import tweepy
import s3fs
import json
from datetime import datetime

def twitter_etl():

    access_key = "***************"
    access_secret = "**************"
    consumer_key = "**************"
    consumer_secret = "**************"

    #twitter authentication
    auth = tweepy.OAuthHandler(access_key,access_secret)
    auth.set_access_token(consumer_key,consumer_secret)

    #twitter object
    api = tweepy.API(auth)
    tweets = api.user_timeline(
        screen_name = '@sundarpichai',
        count = 200,
        include_rts = False,
        tweet_mode = 'extended'
        )
    #print(tweets)

    tweets_list = []

    for tweet in tweets:
        refined_tweet = {
            'user' : tweet.user.screen_name,
            'text' : tweet._json['full_text'],
            'favorite_count' : tweet.favorite_count,
            'created_at' : tweet.created_at
        }

        tweets_list.append(refined_tweet)

    df = pd.DataFrame(tweets_list)
    df.to_csv("s3://c-airflow-bucket/SundarPichai.csv")
