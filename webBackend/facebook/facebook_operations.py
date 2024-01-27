# Authenticate to Twitter
import traceback

import requests


class FacebookOperations:
    # PAT generated via : https://developers.facebook.com/tools/debug/accesstoken/?access_token=EAAUS3ZC4kt8UBAIwD8MZCuWYifieuOE1MZBZCBH9jJYiAjZA2y1fwMXZCRcKoRqaI8vR4RB222RLZAc4n3ZALmZBfGnoIdZBxfLA4PEF6G90vSU2GgQAd2d3Pum6EPFn8XIiYjjZB8XAE7cIQqaZCcbao42PKdvFe1kSfGZBXuFw6HFmFJxJ3xXOcf66as
    page_access_token = 'EAAUS3ZC4kt8UBAIwD8MZCuWYifieuOE1MZBZCBH9jJYiAjZA2y1fwMXZCRcKoRqaI8vR4RB222RLZAc4n3ZALmZBfGnoIdZBxfLA4PEF6G90vSU2GgQAd2d3Pum6EPFn8XIiYjjZB8XAE7cIQqaZCcbao42PKdvFe1kSfGZBXuFw6HFmFJxJ3xXOcf66a'

    def fbpost(self, content=None, link=None):
        try:
            auth_token = self.page_access_token
            hed = {'Authorization': 'Bearer ' + auth_token}
            data = {'message': content, 'link': link}

            url = 'https://graph.facebook.com/v15.0/335718390251345/feed'
            response = requests.post(url, json=data, headers=hed)
            print("FB page : Make me techie" + str(response.status_code))

            # url = 'https://graph.facebook.com/v15.0/949511092391225/feed'  # FB group : Breaking news today
            # response = requests.post(url, json=data, headers=hed)
            # print("FB Page: Breaking news today: " + str(response.status_code))

            url = 'https://graph.facebook.com/v15.0/1033383150117702/feed'  # FB group : USA news
            response = requests.post(url, json=data, headers=hed)
            print("FB Page: Breaking news today: " + str(response.status_code))

            # url = 'https://graph.facebook.com/v15.0/756658668617227/feed'  # FB group : Tech News
            # response = requests.post(url, json=data, headers=hed)
            # print("FB Page: Breaking news today: " + str(response.status_code))
            #
            # url = 'https://graph.facebook.com/v15.0/737906283613706/feed'  # FB group : USA News
            # response = requests.post(url, json=data, headers=hed)
            # print("FB Page: Breaking news today: " + str(response.status_code))
            #
            # url = 'https://graph.facebook.com/v15.0/465510840268838/feed'  # FB group : Tech news Android
            # response = requests.post(url, json=data, headers=hed)
            # print("FB Page: Breaking news today: " + str(response.status_code))
            #
            # url = 'https://graph.facebook.com/v15.0/technews99/feed'  # FB group : Tech_news
            # response = requests.post(url, json=data, headers=hed)
            # print("FB Page: Breaking news today: " + str(response.status_code))

            print("Posted...")
        except Exception as e:
            print(e)
            traceback.print_stack()
