import requests

from src.main.api.configs.config import Config
from src.main.api.models.auth_login_request import AuthLoginRequest
from src.main.api.models.auth_login_response import AuthLoginResponse


class RequestSpecs:
    @staticmethod
    def base_headers():
        return {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }

    @staticmethod
    def auth_headers(username: str, password: str):
        request = AuthLoginRequest(username=username, password=password)
        response = requests.post(
            url='http://localhost:4111/api/auth/token/login',
            json = request.model_dump(),
            headers = RequestSpecs.base_headers()
        )
        if response.status_code == 200:
            response_data = AuthLoginResponse(**response.json())
            token = response_data.token

            headers = RequestSpecs.base_headers()
            headers['Authorization'] = f'Bearer {token}'

            return headers
        raise Exception("Failed to authorization")

    @staticmethod
    def no_auth_headers():
        return RequestSpecs.base_headers()
