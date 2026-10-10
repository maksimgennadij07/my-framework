import pytest
from sqlalchemy.orm import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.db.crud.user_crud import UserCrudDb as User


@pytest.mark.api
class TestCreateUser:
    # Позитивный сценарий создания USER - ОР 201
    def test_create_user_valid(self, api_manager: ApiManager, db_session: Session):
        create_user_request = CreateUserRequest(username="T1101", password="Pas!sw0rd", role="ROLE_USER")
        response = api_manager.admin_steps.create_user(create_user_request)
        # Проверки совпадение значений в запросе и ответе
        assert create_user_request.username == response.username
        assert create_user_request.role == response.role
        # Проверка создания пользователя в БД
        user_from_db = User.get_user_by_username(db_session, create_user_request.username)
        assert user_from_db.username == create_user_request.username

    @pytest.mark.parametrize(
        'username, password',
        [
            ('Никита', 'Pas!sw0rd'), # Негативная проверка - кириллица в логине
            ('GG', 'Pas!sw0rd'), # Негативная проверка - минимум 3 символа
            ('GGGGGGGGGGGGGGGG', 'Pas!sw0rd'), # Негативная проверка - максимум 15 символа
            ('GG1 23', 'Pas!sw0rd'), # Негативная проверка - разрешены цифры и буквы
            ('GG123$$', 'Pas!sw0rd'), # Негативная проверка - запрещены спец символы
            ('GG123', 'Pas!sw0rdпривет'), # Негативная проверка - кириллица в пароле
            ('GG123', 'Pas!sw0'), # Негативная проверка - минимум 8 символов
            ('GG123', 'as!sw0rd'), # Негативная проверка - минимум 1 заглавная буква
            ('GG123', 'PAS!SW0RD'), # Негативная проверка - минимум 1 мальнькая буква
            ('GG123', 'Passw0rd'), # Негативная проверка - минимум 1 спец символ
            ('GG123', 'Pas!swrd'), # Негативная проверка - минимум 1 цифра
        ]
    )
    # Создание пользователя с некорректными данными
    def test_create_user_invalid_400(self, username: str, password: str, api_manager: ApiManager, db_session: Session):
        create_user_request = CreateUserRequest(username= username, password= password, role="ROLE_USER")
        api_manager.admin_steps.create_user_invalid_400(create_user_request)
        #
        user_from_db = User.get_user_by_username(db_session, create_user_request.username)
        assert user_from_db is None, 'User created - Error'

    def test_create_user_invalid_401(self, api_manager: ApiManager, db_session: Session):
        create_user_request = CreateUserRequest(username="T100", password="Pas!sw0rd", role="ROLE_USER")
        api_manager.admin_steps.create_user_invalid_401(create_user_request)

        user_from_db = User.get_user_by_username(db_session, create_user_request.username)
        assert user_from_db is None, 'User created - Error'