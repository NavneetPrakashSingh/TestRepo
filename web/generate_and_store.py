import datetime
import json
import os

import requests

from webBackend.nltkOperations import NltkOperations


class GenerateAndStore:
    current_directory = os.path.abspath(os.path.join(os.path.realpath(__file__), ".."))
    date_file = os.path.abspath(os.path.join(current_directory, "data", "date.json"))
    data_directory = os.path.abspath(os.path.join(current_directory, "data"))
    news_directory = os.path.abspath(os.path.join(current_directory, "data", "news"))
    STAGING_URL = "https://api.npoint.io/c431b7087ec7f48eff54"
    PROD_URL = "https://newsapi.org/v2/everything?q=technology&sources=associated-press,ars-technica,axios,cnn,techcrunch&sortBy=popularity&from=%s&to=%s&pageSize=12&page=1&apiKey=2091bf4714d3486d9f9ef80346ad60f8&language=en"
    ALT_PROD_URL = "https://newsapi.org/v2/everything?q=technology&sources=associated-press,ars-technica,axios,techcrunch&sortBy=popularity&from=%s&to=%s&pageSize=12&page=1&apiKey=2091bf4714d3486d9f9ef80346ad60f8&language=en"
    URLS = [
        'https://newsapi.org/v2/top-headlines?category=business&apiKey=2091bf4714d3486d9f9ef80346ad60f8&language=en',
        'https://newsapi.org/v2/top-headlines?category=technology&apiKey=2091bf4714d3486d9f9ef80346ad60f8&language=en',
        'https://newsapi.org/v2/top-headlines?category=entertainment&apiKey=2091bf4714d3486d9f9ef80346ad60f8&language=en']

    def generate(self):

        # Read the sources one by one and put them in the respective files
        # categories = ['business', 'technology', 'entertainment']
        categories = ['entertainment']
        for category in categories:
            url = 'https://newsapi.org/v2/top-headlines?category=' + category + '&apiKey=2091bf4714d3486d9f9ef80346ad60f8&language=en&country=us'
            resp = requests.get(url=url)
            data = resp.json()
            if data['totalResults'] == 0:
                print("No results for the day")
                break
            index = 0
            include_in_ouput = True
            output = []
            print("Generating summary for " + str(len(data['articles'])) + " articles")
            articles_collection = data['articles']
            # while len(articles_collection) > 10:
            #     articles_collection.pop()
            print(len(articles_collection))
            for article in articles_collection:
                try:
                    include_in_ouput = True
                    # Remove all non-ascii-characters, makes it difficult to parse
                    article['title'] = NltkOperations.clean(article['title'])
                    article['description'] = NltkOperations.clean(article['description'])
                    article['url'] = NltkOperations.remove_non_ascii(article['url'])
                    article['content'] = NltkOperations.clean(article['content'])
                    article_url = NltkOperations.remove_non_ascii(article['url'])
                    summary = NltkOperations.get_summary(article_url, "none")
                    if summary is None or summary[0] is '':
                        index = index + 1
                        include_in_ouput = False
                        continue
                    data['articles'][index]['summary'] = summary[0]
                    data['articles'][index]['html_summary'] = summary[1]
                    data['articles'][index]['website_url'] = article['url']
                    data['articles'][index]['url'] = "/" + datetime.datetime.today().strftime(
                        '%Y-%m-%d') + "-" + NltkOperations.get_url(article['url'])
                except Exception as e:
                    index = index + 1
                    include_in_ouput = False
                    print(e)
                    continue
                if include_in_ouput:
                    output.append(data['articles'][index])
                index = index + 1
                include_in_ouput = True
            file_name = category + "-news" + ".json"
            # Add page description for news
            page_title = "Latest "+category+" news for today in 10 minutes"
            for article in data['articles']:
                page_title = page_title + ". " + article['title']
            data['page_description'] = page_title
            with open(os.path.join(self.data_directory, file_name), 'w', encoding='utf-8') as f:
                json.dump(output, f, ensure_ascii=False, indent=4)
            print("File stored at :" + os.path.join(self.data_directory, file_name))

        # Merge apple-news and entertainment-news together in news.json
        business_news_path = os.path.abspath(os.path.join(self.data_directory, "business-news.json"))
        business_news = None
        if os.path.exists(business_news_path):
            f = open(business_news_path)
            business_news = json.load(f)

        technology_news_path = os.path.abspath(os.path.join(self.data_directory, "technology-news.json"))
        technology_news = None
        if os.path.exists(technology_news_path):
            f = open(technology_news_path)
            technology_news = json.load(f)

        merged = technology_news + business_news
        file_name = "news.json"
        with open(os.path.join(self.data_directory, file_name), 'w', encoding='utf-8') as f:
            json.dump(merged, f, ensure_ascii=False, indent=4)
        print("File stored at :" + os.path.join(self.data_directory, file_name))

    # def generate(self):
    #     # Read start and end date from date.json
    #     f = open(self.date_file)
    #     data_date = json.load(f)
    #     last_run = data_date['news']
    #     while datetime.datetime.strptime(last_run, "%Y-%m-%d").date() <= datetime.date.today():
    #         end_date = datetime.datetime.strptime(last_run, "%Y-%m-%d") + datetime.timedelta(days=1)
    #         prod_url = self.ALT_PROD_URL % (str(last_run), str(end_date.date()))
    #         print(prod_url)
    #         resp = requests.get(url=prod_url)
    #         data = resp.json()
    #         if data['totalResults'] == 0:
    #             print("No results for the day")
    #             break
    #         index = 0
    #         del_indexes = []
    #         print("Generating summary for " + str(len(data['articles'])) + " articles")
    #         for article in data['articles']:
    #             # Remove all non-ascii-characters, makes it difficult to parse
    #             article['title'] = NltkOperations.clean(article['title']) + ""
    #             article['description'] = NltkOperations.clean(article['description'])
    #             article['url'] = NltkOperations.remove_non_ascii(article['url'])
    #             article['content'] = NltkOperations.clean(article['content'])
    #             article_url = NltkOperations.remove_non_ascii(article['url'])
    #             summary = NltkOperations.get_summary(article_url, "ml")
    #             if summary is None or summary[0] is '':
    #                 del_indexes.append(index)
    #                 index = index + 1
    #                 continue
    #             data['articles'][index]['summary'] = summary[0]
    #             data['articles'][index]['html_summary'] = summary[1]
    #             data['articles'][index]['website_url'] = article['url']
    #             data['articles'][index]['url'] = "/" + last_run + "-" + NltkOperations.get_url(article['url'])
    #             index = index + 1
    #         file_name = last_run + ".json"
    #         if del_indexes:
    #             del_indexes = sorted(del_indexes, reverse=True)  # Need to sort and remove higher indexes first
    #             for values in del_indexes:
    #                 del data['articles'][values]
    #         # Add page description for news
    #         page_title = "Latest news for today in 10 minutes"
    #         for article in data['articles']:
    #             page_title = page_title + ". " + article['title']
    #         data['page_description'] = page_title
    #         with open(os.path.join(self.news_directory, file_name), 'w', encoding='utf-8') as f:
    #             json.dump(data, f, ensure_ascii=False, indent=4)
    #         last_run = end_date.strftime("%Y-%m-%d")
    #         data_date["news"] = end_date.date().strftime("%Y-%m-%d")
    #         with open(self.date_file, "w") as jsonFile:
    #             json.dump(data_date, jsonFile)
    #         print("File stored at :" + os.path.join(self.news_directory, file_name))
    #     print("Tool completed successfully")
    #     # Make request to URL and get the data for news on that day
    #
    #     # Generate summary for each news article with the details
    #     # Store it in date.json
