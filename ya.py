import requests
from collections import Counter
from pprint import pprint
from tqdm import tqdm
import time

class YaUploader:
    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {
            'Accept': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def _get_upload_link(self, disk_file_path):
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = self.get_headers()
        params = {"path": disk_file_path, "overwrite": "true"}
        response = requests.get(upload_url, headers=headers, params=params)
        data = response.json()
        url_to_load = data.get('href')
        return url_to_load

    def new_folder(self, folder_name):
        print(f'Имя новой папки на Я-диск - "{folder_name}"')
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        head = self.get_headers()
        params = {'path': f'disk:/{folder_name}'}

        response = requests.put(url, params=params, headers=head)
        if response.status_code in [201, 409]:
            print('Новая папка создана')
            return folder_name
        print('Folder_error', response.json()['error']['error_msg'])

    def upload_photo(self, photos, folder_name):
        folder = self.new_folder(folder_name=folder_name)
        like_list = []
        log_dict = []
        for photo in tqdm(photos, sesc='Processing photos', unit='photo'):
            url = photo['url']
            date = photo['date']
            likes = photo['likes']
            name = f'{likes}likes.jpg'
            like_list.append(likes)
            counter = Counter(like_list)
            for v in counter.values():
                if v > 1:
                    name = f'{likes}likes{date}.jpg'
            path = f'{folder}/{name}'
            href = self._get_upload_link(path)
            response = requests.get(url)
            data = response.content
            resp = requests.put(href, data=data)

        return log_dict
