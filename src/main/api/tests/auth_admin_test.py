from urllib import response

import pytest
from src.main.api.models.auth_login_request import AuthLoginRequest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.requests.login_user_requester import LoginUserRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.requests.create_user_requester import CreateUserRequester


@pytest.mark.api
class TestAuthAdmin:
    # Позитивная проверка авторизации ADMIN
    def test_auth_admin_valid(self, api_manager):

        auth_admin_request = AuthLoginRequest(username="admin", password="123456")
        response = api_manager.admin_steps.login_user(auth_admin_request)
        assert auth_admin_request.username == response.user.username
        assert response.user.role == "ROLE_ADMIN"

    @pytest.mark.parametrize(
        'username,password',
        [
            ('','123456'), # Отсутствует логин - ОР 400
            ('admin', ''), # Отсутствует пароль - ОР 400
        ]
    )

    # Негативная проверка авторизации ADMIN - ОР 400
    def test_auth_admin_invalid_400(self, username, password, api_manager):
        auth_admin_request = AuthLoginRequest(username=username, password=password)
        api_manager.admin_steps.login_user_invalid_400(auth_admin_request)

    @pytest.mark.parametrize(
        'username,password',
        [
            ('admin', '123455'),  # Некорректный пароль - ОР 401
            ('adnim', '123456'),  # Неорректный логин - ОР 401
        ]
    )
    # Негативная проверка авторизации ADMIN - ОР 401
    def test_auth_admin_invalid_401(self, username, password, api_manager):
        auth_admin_request = AuthLoginRequest(username= username, password= password)
        api_manager.admin_steps.login_user_invalid_401(auth_admin_request)

# Проверки пользователя
    def test_auth_admin_create_user_auth_user_valid(self, api_manager, create_user_request):

        # Создание пользователя
        response = api_manager.admin_steps.login_user(create_user_request)

        assert response.user.username == create_user_request.username
        assert response.user.role == create_user_request.role

    # Некорректная авторизация под пользователем, некорректный пароль
    def test_auth_admin_create_user_auth_user_invalid(self, api_manager, create_user_request):
        auth_admin_request = AuthLoginRequest(username= "T100", password= 'Pas!sw0rd')
        api_manager.admin_steps.login_user_invalid_401(auth_admin_request)
