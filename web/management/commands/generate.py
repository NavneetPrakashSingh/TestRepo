from django.core.management.base import BaseCommand

from web.generate_and_store import GenerateAndStore
from web.generate_apple_news import GenerateAppleNews
from webBackend.nltkOperations import NltkOperations


class Command(BaseCommand):
    help = 'Generate and parses summary for the news app'

    def handle(self, **options):
        try:
            NltkOperations.pre_build()
            genObj = GenerateAndStore()
            genObj.generate()

            generate_apple_news = GenerateAppleNews()
            generate_apple_news.generate()
        except Exception as e:
            print(e)
