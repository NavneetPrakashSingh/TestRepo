import datetime
import json
import os

import math
import requests
from django.core.management.base import BaseCommand

from webBackend.facebook.facebook_operations import FacebookOperations
from webBackend.twitter.twitter_operations import TwitterOperations


class Command(BaseCommand):
    help = 'Tweet and Post News'
    current_directory = os.path.abspath(os.path.join(os.path.realpath(__file__), ".."))
    tweet_config_file = os.path.abspath(os.path.join(current_directory, "..", "..", "data", "tweet.json"))
    news_data_file = os.path.abspath(os.path.join(current_directory, "..", "..", "data", "news"))

    def handle(self, **options):
        try:
            print(" -- Tweet started -- ")
            f = open(self.tweet_config_file)
            tweet_config = json.load(f)
            tweet_date = tweet_config["tweet_date"]
            tweet_index = int(tweet_config["tweet_index"])
            file_name = tweet_date + ".json"
            news_file_path = os.path.join(self.news_data_file, file_name)
            if os.path.exists(news_file_path):
                print("Opening for path :" + str(news_file_path))
                n_f = open(news_file_path)
                news_data = json.load(n_f)
                news_article = news_data['articles'][int(tweet_index)]
                news_title = news_data['articles'][int(tweet_index)]['title']
                truncated_news_title = (news_title[:170] + '...') if len(news_title) > 170 else news_title[:170]
                news_link = "https://makemetechie.com" + news_article['url']
                print("Searching for news link: "+ news_link)
                r = requests.get(news_link)
                if r.status_code == 200:
                    print(" Status 200 for the link " + str(news_link))
                    twitter_obj = TwitterOperations()
                    # hashtags = twitter_obj.get_trending_hashtags()
                    words_per_minute = math.ceil(len(news_article['summary'].split(' ')) / 170)
                    # news_content = "Tired of long #news articles? Read #summary for the latest #news article in " + str(
                    #     words_per_minute) + " min or less. \n #tech #technology #news \n @BBCBreaking @cnnbrk @ABC @NBCNews\n Read summary by clicking the card ⬇️" + news_link
                    news_content = "✋‼️ #Trending #news for the hour: " + truncated_news_title + " \n Read news #summaries by clicking the card 👇⬇️ \n https://www.makemetechie.com/news"
                    twitter_obj.tweet(news_content)
                    fb_content = "Read #summary for the latest #news article in " + str(
                        words_per_minute) + " min or less. We post summaries every day. Today's summary is about " + \
                                 news_article["title"] + "\n Read summary by clicking the card ⬇️"
                    fb_obj = FacebookOperations()
                    fb_obj.fbpost(fb_content, news_link)
                    new_index = tweet_index + 1
                    if new_index > len(news_data['articles']) - 1:
                        next_day = datetime.datetime.strptime(tweet_date, "%Y-%m-%d") + datetime.timedelta(days=1)
                        tweet_config['tweet_date'] = next_day.date().strftime("%Y-%m-%d")
                        tweet_config['tweet_index'] = 0
                    else:
                        tweet_config['tweet_index'] = new_index
                    # News tweeted successfully, update date in tweet.json
                    with open(self.tweet_config_file, "w") as jsonFile:
                        json.dump(tweet_config, jsonFile)
                    print("File stored at :" + os.path.join(self.tweet_config_file))
                else:
                    print("Status isn't 200, try again in an hour...")
        except Exception as e:
            print(e)
