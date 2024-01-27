# Authenticate to Twitter
import random
import traceback

import tweepy as tweepy

class TwitterOperations:
    consumer_key = 'hps5BnlU9YvJHskN12c3XmLcs'
    consumer_secret = '7Kyvs1SwEcf3oecHSK4VQzJmbFju5SByH8jjG292Wq3JnyMkNn'
    access_token = '1578222511980187649-C5VNqQz5YhGcUBF3WfIdqpZ9vWllam'
    access_token_secret = 'tUc0CaEBlI4921a524cqNryJUuTipGp9mPtTv2q0OSJ3N'
    woeid = [23424977,2367105, 2391279, 2442047 , 2452078 , 2459115 , 2475687 ]

    def get_trending_hashtags(self):
        try:
            # authorization of consumer key and consumer secret
            auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)

            # set access to user's access key and access secret
            auth.set_access_token(self.access_token, self.access_token_secret)

            # calling the api
            api = tweepy.API(auth)

            # fetching the trends
            rand_woeid = random.choice(self.woeid)
            trends = api.get_place_trends(id=rand_woeid)

            # printing the information
            print("The top trends for the location are :")

            tmp = ""
            index = 0
            for value in trends:
                for trend in value['trends']:
                    if index >5:
                        break
                    if "#" not in trend['name']:
                        trend['name'] = "#"+trend['name']
                    tmp = tmp +" "+ trend['name'].replace(" ","")
                    index = index + 1
            tmp += " #tech #technology #news #trending"
            return tmp
        except Exception as e:
            print(e)

    def tweet(self, content):
        try:
            # Authenticate to Twitter

            client = tweepy.Client(consumer_key=self.consumer_key, consumer_secret=self.consumer_secret,
                                   access_token=self.access_token, access_token_secret=self.access_token_secret)

            # Create a tweet
            result = client.create_tweet(text=content)
            tweet_id = result.data['id']
            print("Tweeted...")

            #Retweet via tweet_navneet
            ns_consumer_key = "CI8NWLKrG8LKQqAemZW5NfAsc"
            ns_consumer_secret = "ZC2JMrAsrGQTYnOm9S6xIS5iWOaUvf77v0LrpavQaA5C7sVm8w"
            ns_access_token = "2493092468-1TXXBDsjukJHPV2sCLk21gJcyJ2G20iuXuxlsto"
            ns_access_token_secret = "PB9nJHCywQCYziBID1kJccVTta2tBKbSj9ekKfh2MBJVE"
            auth = tweepy.OAuthHandler(ns_consumer_key, ns_consumer_secret)
            auth.set_access_token(ns_access_token, ns_access_token_secret)
            # calling the api
            api = tweepy.API(auth)

            # the ID of the tweet to be retweeted
            ID =tweet_id

            # retweeting the tweet
            api.retweet(ID)
            print("Retweeted...")
        except Exception as e:
            print(e)
            traceback.print_stack()
