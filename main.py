from ya import YaUploader
from vk import Vk
import os
from os.path import join, dirname
from dotenv import load_dotenv
from pprint import pprint

if __name__ == '__main__':
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)
    VKTOKEN = os.environ.get("VKTOKEN")
    YATOKEN = os.environ.get("YATOKEN")
    vk = Vk(token=VKTOKEN)
    ya = YaUploader(token=YATOKEN)
    name = input('Введите id или nickname в VK:')
    count = input('Сколько фото вы хотите загрузить?')
    folder = input('Введите название папки, в которую хотите сохранить фото:')
    photo_dict = vk.get_photos(name, count)
    if photo_dict != "error":
        log_dict = ya.upload_photo(photo_dict, folder)
        print(f'Фото из аккаунта {name} успешно скопированы на Яндекс-диск')
        print(f'Информация о сохранённых на Я-диск фото:')
        pprint(log_dict)






