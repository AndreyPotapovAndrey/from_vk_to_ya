import requests
from collections import Counter
from pprint import pprint
from alive_progress import alive_bar
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

        requests.put(url, params=params, headers=head)
        print('Новая папка создана')

        return folder_name

    # def create_folder(path):
    #     """Создание папки. \n path: Путь к создаваемой папке."""
    #     requests.put(f'{URL}?path={path}', headers=head)

    def upload_to_disk(self, file, text, folder_name):
        folder = self.new_folder(folder_name=folder_name)
        path = f'{folder}/{file}'

        href = self._get_upload_link(path)
        response = requests.put(href, data=open(text, 'rb'))
        pprint(response)
        if response.status_code == 201:
            print('Файл успешно сохранён на Я-диск')

    def upload_photo(self, photos, folder_name):
        folder = self.new_folder(folder_name=folder_name)
        like_list = []
        log_dict = []
        for photo in photos:
            url = photo['url']
            date = photo['date']
            likes = photo['likes']
            name = f'{likes}likes.jpg'
            like_list.append(likes)
            # pprint(photo)
            # pprint(like_list)
            # pprint(date)
            counter = Counter(like_list)
            for v in counter.values():
                if v > 1:
                    name = f'{likes}likes{date}.jpg'
            # pprint(name)
            log_dict.append({'file_name': name, 'size': photo['type']})
            path = f'{folder}/{name}'
            href = self._get_upload_link(path)
            response = requests.get(url)
            data = response.content
            resp = requests.put(href, data=data)
            if resp.status_code == 201:
                with alive_bar(len(photos)) as bar:
                    for _ in photos:
                        bar()
                        time.sleep(1)
        return log_dict
