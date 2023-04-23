import requests
import os
from os.path import join, dirname
from dotenv import load_dotenv
from pprint import pprint


class Vk:
    url = 'https://api.vk.com/method/'

    def __init__(self, token):
        self.params = {
            'access_token': token,
            'v': '5.131'
        }

    def get_photos(self, user_id, count):
        # get user info
        user_url = self.url + 'users.get'
        user_params = {
            'user_ids': user_id,
            'fields': 'is_closed'
        }
        user_data = requests.get(user_url, params={**self.params, **user_params}).json()
        pprint(user_data)

        # check if user exists
        if 'response' in user_data:
            user_id = user_data['response'][0]['id']
        else:
            return None

        # check if user is closed
        if user_data['response'][0].get('is_closed'):
            print("User is closed")

        # get album photos
        photos_url = self.url + 'photos.get'
        photos_params = {
            'owner_id': user_id,
            'album_id': 'profile',
            'rev': 1,
            'extended': 1,
            'photo_sizes': 1,
            # 'count': count
            'access_key': 0
        }
        response = requests.get(photos_url, params={**self.params, **photos_params}).json()

        if response.get('error'):
            print('ERROR', response['error']['error_msg'])
            return 'error'
        elif response['response']['count'] == 0:
            print('There are no photos from clients profile')
            return 'error'

        # process each photo and collect data with the best quality photo
        photos = []
        for photo in response.get('response', {}).get('items', []):
            sizes = sorted(photo.get('sizes', []), key=lambda x: x.get('type', 'x'))

            # get image url with the highest resolution
            max_size = max(sizes, key=lambda x: x.get('height') * x.get('width'))

            likes = photo.get('likes', {}).get('count')
            url = max_size.get('url', '')
            date = photo.get('date')

            # create a letter to denote the size of the largest photo
            letter = max_size.get('type', '').upper()[0]
            if url != " ":
                photos.append({'date': date, 'likes': likes, 'type': letter, 'url': url})
        sorted_photos = sorted(photos, key=lambda x: (x['type'], x['likes']), reverse=True)

        return sorted_photos[:int(count)]

