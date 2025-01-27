import base64
from dataclasses import dataclass
import requests

from settings import Settings
from shema import YandexUserData


@dataclass
class YandexClient:
    settings: Settings

    def get_user_info(self, code: str) -> YandexUserData:
        access_token = self._get_user_access_token(code=code)
        user_info = requests.get('https://login.yandex.ru/info?format=json',
                                 headers={'Authorization': f'OAuth {access_token}'})
        return YandexUserData(**user_info.json(), access_token=access_token)

    def _get_user_access_token(self, code: str) -> str:
        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'client_id': self.settings.YANDEX_CLIENT_ID,
            'client_secret': self.settings.YANDEX_CLIENT_SECRET,
        }
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        response = requests.post(self.settings.YANDEX_TOKEN_URL, data=data, headers=headers)
        access_token = response.json()['access_token']
        return access_token
