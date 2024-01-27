import datetime
import json
import os

import requests

from webBackend.nltkOperations import NltkOperations


class GenerateAppleNews:
    current_directory = os.path.abspath(os.path.join(os.path.realpath(__file__), ".."))
    date_file = os.path.abspath(os.path.join(current_directory, "data", "date.json"))
    apple_news_directory = os.path.abspath(os.path.join(current_directory, "data", "apple-news.json"))
    STAGING_URL = "https://api.npoint.io/c431b7087ec7f48eff54"
    PROD_URL = "https://newsapi.org/v2/everything?q=apple&sortBy=popularity&from=%s&to=%s&pageSize=50&page=1&apiKey=2091bf4714d3486d9f9ef80346ad60f8&language=en"
    ALT_PROD_URL = "https://newsapi.org/v2/everything?q=technology&sources=associated-press,ars-technica,axios,techcrunch&sortBy=popularity&from=%s&to=%s&pageSize=12&page=1&apiKey=2091bf4714d3486d9f9ef80346ad60f8&language=en"

    def generate(self):
        try:
            # Open and read app news directory
            # If the data is not present append it
            f = open(self.apple_news_directory)
            apple_news_data = json.load(f)
            prod_url = self.PROD_URL % (
            str((datetime.datetime.today() + datetime.timedelta(days=-1)).date()), str(datetime.datetime.today().date()))
            # prod_url = self.STAGING_URL
            print(prod_url)
            resp = requests.get(url=prod_url)
            data = resp.json()

            del_indexes = []
            output_arr = []
            count = 0
            for article in data['articles']:
                if len(output_arr) > 10:
                    break
                article['title'] = NltkOperations.clean(article['title'])
                ans = False
                for items in apple_news_data:
                    # Check if data already exists in news data file, don't parse it
                    if items['title'] == article['title']:
                        ans = True
                if ans:
                    print("Skipping article with title :" + article['title'])
                    continue
                print("Printing news for article : " + article['title'])
                count = count + 1
                # Remove all non-ascii-characters, makes it difficult to parse
                current_element = {}
                current_element['author'] = article['author']
                current_element['source'] = article['source']
                current_element['urlToImage'] = article['urlToImage']
                current_element['publishedAt'] = article['publishedAt']
                current_element['title'] = NltkOperations.clean(article['title'])
                current_element['description'] = "Makemetechie.com | Summary : " + NltkOperations.clean(
                    article['description'])
                current_element['url'] = NltkOperations.remove_non_ascii(article['url'])
                current_element['content'] = NltkOperations.clean(article['content'])
                article_url = NltkOperations.remove_non_ascii(article['url'])
                summary = NltkOperations.get_summary(article_url, "none")
                if summary is None or summary[0] is '':
                    continue
                current_element['summary'] = summary[0]
                current_element['html_summary'] = summary[1]
                current_element['website_url'] = article['url']
                current_element['url'] = "/" + str(datetime.datetime.today().date()) + "-" + NltkOperations.get_url(
                    article['url'])
                output_arr.append(current_element)

            total_number_of_articles = len(apple_news_data) + len(output_arr)
            if total_number_of_articles > 25:
                items_to_remove = total_number_of_articles - 25
                while items_to_remove > 0:
                    apple_news_data.pop()
                    items_to_remove = items_to_remove - 1

            final = output_arr + apple_news_data
            with open(os.path.join(self.apple_news_directory), 'w', encoding='utf-8') as f:
                json.dump(final, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(e)
