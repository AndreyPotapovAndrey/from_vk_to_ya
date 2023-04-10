import requests


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

        # check if user exists
        if 'response' in user_data:
            user_id = user_data['response'][0]['id']
        else:
            return None

        # check if user is closed
        if user_data['response'][0].get('is_closed'):
            return "User is closed"

        # get album photos
        photos_url = self.url + 'photos.get'
        photos_params = {
            'owner_id': user_id,
            'album_id': 'profile',
            'rev': 1,
            'extended': 1,
            'photo_sizes': 1,
            'count': count,
            'access_key': 0
        }
        response = requests.get(photos_url, params={**self.params, **photos_params}).json()

        # process each photo and collect data with the best quality photo
        photos = []
        photo_found = False
        for photo in response.get('response', {}).get('items', []):
            sizes = sorted(photo.get('sizes', []), key=lambda x: x.get('type', 'a'))

            # get image url with the highest resolution
            max_size = max(sizes, key=lambda x: x.get('height') * x.get('width'))

            likes = photo.get('likes', {}).get('count')
            url = max_size.get('url', '')
            date = photo.get('date')

            # create a letter to denote the size of the largest photo
            letter = max_size.get('type', '').upper()[0]

            photos.append({'date': date, 'likes': likes, 'type': letter, 'url': url})
            photo_found = True

        if not photo_found:
            return "No photos found in the 'profile' album with specified size."

        return photos

