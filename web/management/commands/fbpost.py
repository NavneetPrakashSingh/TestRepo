import datetime
import json
import os

import math
import requests
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Tweet News'
    current_directory = os.path.abspath(os.path.join(os.path.realpath(__file__), ".."))
    tweet_config_file = os.path.abspath(os.path.join(current_directory,"..","..", "data", "tweet.json"))
    news_data_file = os.path.abspath(os.path.join(current_directory,"..","..","data","news"))

    def handle(self, **options):
        try:
            url = "https://graph.facebook.com/335718390251345/feed?message=Hello from the API&access_token=EAAUS3ZC4kt8UBAGFfKhcjkPxmeNvBHsqK3ibxZAIS8xl6OivSlZC51L5HWlWtsZCetjT8mJzUj8IASzlw8fZAs07gdlYdOcuP9qCYbFPGJprwcSgDZCm24pbZBfVm0J8brD7RjGDrtZCkZBBTddUUZBqZCoHlV7xTNI6wZAUo2zZCaHgQ4x8z8lomVXsM"

            x = requests.post(url)
            print(x)
        except Exception as e:
            print(e)
