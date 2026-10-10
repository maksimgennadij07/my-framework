import pytest
from sqlalchemy.orm import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import  AccountCrudDb as Account
from src.main.api.fixtures.db_fixture import db_session
from src.main.api.models.create_user_request import CreateUserRequest


@pytest.mark.api
class TestCreateAccount:
    # Позитивная проверка создания банковского счёта
    def test_create_bank_check_valid(self, api_manager: ApiManager, create_user_request: CreateUserRequest, db_session: Session):
        response = api_manager.user_steps.create_account(create_user_request)
        # Проверка соответствия ответа логике
        assert response.balance == 0
        # Проверки создания аккаунта в БД
        account_from_db = Account.get_account_by_id(db_session, response.id)
        assert account_from_db.id == response.id, 'Account not created, ID not in DB'
        assert account_from_db.balance is not None, 'Account not created, balance is None'

    # Негативная проверка создания банковского счёта из учетки админа
    def test_create_bank_check_invalid(self, api_manager: ApiManager, db_session: Session):
        before_count = Account.count_all(db_session)
        api_manager.user_steps.create_account_invalid_403()
        after_count = Account.count_all(db_session)
        assert after_count == before_count, 'Account created - Error'