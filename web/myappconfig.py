# my_app/apps.py

from django.apps import AppConfig

from webBackend.nltkOperations import NltkOperations


class MyAppConfig(AppConfig):
    name = 'web'

    def ready(self):
        NltkOperations.pre_build()
        # put your startup code here

