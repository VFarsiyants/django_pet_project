import requests
from datetime import datetime
from os import path

from social_core.exceptions import AuthForbidden


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'google-oauth2':
        return

    base_url = 'https://people.googleapis.com/v1/people/me'
    params = {
        'access_token': response['access_token'],
        'personFields': 'names,photos,genders,birthdays'
    }

    api_response = requests.get(base_url, params=params)
    if api_response.status_code != 200:
        return

    api_data = api_response.json()

    if 'genders' in api_data and user.shopuserprofile.gender == 'U':
        gender_key = api_data['genders'][-1]['formattedValue'][0]
        if gender_key in ('M', 'F'):
            user.shopuserprofile.gender = gender_key
        else:
            user.shopuserprofile.gender = 'U'

    if 'birthdays' in api_data:
        day = api_data['birthdays'][-1]['date']['day']
        month = api_data['birthdays'][-1]['date']['month']
        year = api_data['birthdays'][-1]['date']['year']
        today = datetime.now()
        age = today.year - year - ((today.month, today.day) < (month, day))
        if age < 18:
            user.delete()
            raise AuthForbidden('social_core.backends.google.GoogleOAuth2')
        user.age = age

    if 'photos' in api_data:
        url = api_data['photos'][-1]['url']
        photo_base_path = url.split('/')[-1]
        google_photo_path = f'users/{photo_base_path}'
        if not path.exists(f'media/{google_photo_path}'):
            photo = requests.get(url=api_data['photos'][-1]['url'])
            with open(f'media/{google_photo_path}', 'wb') as photo_f:
                photo_f.write(photo.content)
            user.avatar = google_photo_path
    user.save()
