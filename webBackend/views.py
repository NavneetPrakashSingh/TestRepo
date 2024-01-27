import json
import datetime
import os

import requests
from django.http import HttpResponse
from webBackend.nltkOperations import NltkOperations

current_directory = os.path.abspath(os.path.join(os.path.realpath(__file__), "..", "..", "web"))


def index(request):
    if request.method == 'POST':
        url = request.POST.get("url", "")
        if url is not None:
            NltkOperations.pre_build()
            s = NltkOperations.get_summary(url)
            if len(s) > 1:
                s = {"text": s[0], "html": s[1]}
            summary = HttpResponse(json.dumps(s))
            summary["Content-Type"] = "application/json"
            summary["Access-Control-Allow-Origin"] = "*"
            return summary
        else:
            return HttpResponse("No summary available")


def get_news_data(request):
    try:
        if request.method == 'GET':
            file_path = os.path.abspath(os.path.join(current_directory, "data", "news.json"))
            if os.path.exists(file_path):
                f = open(file_path)
                data = json.load(f)
                return HttpResponse(json.dumps(data), content_type="application/json")
            return HttpResponse("File not ready for the current date")
    except Exception as e:
        return HttpResponse("Something went wrong, try again later")


def get_news_from_range(request):
    try:
        if request.method == 'GET':
            start_date = request.GET.get("start_date")
            end_date = request.GET.get("end_date")
            start_date_obj = datetime.datetime.strptime(start_date, '%Y-%m-%d')
            end_date_obj = datetime.datetime.strptime(end_date, '%Y-%m-%d')
            if start_date_obj > end_date_obj:
                return HttpResponse("Invalid date range")

            days = (end_date_obj - start_date_obj).days
            print(days)
            date_list = [end_date_obj - datetime.timedelta(days=x) for x in range(days + 1)]
            articles = []
            for date in reversed(date_list):
                file_path = os.path.abspath(os.path.join(current_directory, "data", "news", str(date.date()) + ".json"))
                if os.path.exists(file_path):
                    f = open(file_path)
                    data = json.load(f)
                    articles.append(data['articles'])

            flat_list = [item for sublist in articles for item in sublist]

            return HttpResponse(json.dumps(flat_list), content_type="application/json")
    except Exception as e:
        return HttpResponse("Something went wrong, try again later")


def generate(request):
    if request.method == 'POST' and 'startDate' in request.POST:
        json_data = json.loads(request.body)
        start_date = json_data['startDate']
        if 'endDate' not in request.POST:
            start_date_in_datetime = datetime.datetime.strptime(start_date, '%Y-%m-%d')
            end_date = start_date_in_datetime + datetime.timedelta(days=1)
        r = requests.get('https://api.github.com/user')
        print(json_data['url'])
        return HttpResponse(NltkOperations.get_summary(json_data['url']))
    else:
        return HttpResponse("Mandatory field missing")


def hello(request):
    if request.method == 'POST':
        return HttpResponse(request.POST.get("url"))
    s1 = NltkOperations
    s2 = NltkOperations
    if id(s1) == id(s2):
        return HttpResponse("Same")
    else:
        return HttpResponse("Different")


def get_apple_news(request):
    if request.method == 'GET':
        file_path = os.path.abspath(os.path.join(current_directory, "data", "apple-news.json" ))
        if os.path.exists(file_path):
            f = open(file_path)
            data = json.load(f)
            return HttpResponse(json.dumps(data), content_type="application/json")
        return HttpResponse("File not ready for the current date")


def get_entertainment_news(request):
    if request.method == 'GET':
        file_path = os.path.abspath(os.path.join(current_directory, "data", "entertainment-news.json"))
        if os.path.exists(file_path):
            f = open(file_path)
            data = json.load(f)
            return HttpResponse(json.dumps(data), content_type="application/json")
        return HttpResponse("File not ready for the current date")