import pytest
from sqlalchemy.orm import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import  AccountCrudDb as Account
from src.main.api.fixtures.db_fixture import db_session


@pytest.mark.api
class TestDepositAccount:
    # Позитивный сценарий пополнения банковского счёта
    def test_deposit_account_valid(self, api_manager: ApiManager, deposit_account_request, db_session: Session):
        create_user, deposit_account = deposit_account_request
        response = api_manager.user_steps.deposit_account(create_user, deposit_account)
        assert deposit_account.accountId == response.id
        assert deposit_account.amount == response.balance
        balance_db = Account.get_account_by_id(db_session, deposit_account.accountId)
        assert balance_db.balance == deposit_account.amount, 'The balance in the DB does not match the top-up amount'

    # Негативная проверка - ОР 400 (неправильный id счёта)
    def test_deposit_account_invalid_400(self, api_manager: ApiManager, deposit_account_invalid_request_400, db_session: Session):
        create_user, deposit_account = deposit_account_invalid_request_400
        balance_before = Account.get_account_by_id(db_session, deposit_account.accountId)
        api_manager.user_steps.deposit_account_invalid_400(create_user, deposit_account)
        balance_after = Account.get_account_by_id(db_session, deposit_account.accountId)
        assert balance_before is not None, 'The account must exist in the DB'
        assert balance_before.balance == balance_after.balance, 'The balance should not change with error 400'

    # Негативная проверка - ОР 401 (нет токена авторизации при пополнении)
    def test_deposit_account_invalid_401(self, api_manager, deposit_account_invalid_request_401, db_session: Session):
        balance_before = Account.get_account_by_id(db_session, deposit_account_invalid_request_401.accountId)
        api_manager.user_steps.deposit_account_invalid_401(deposit_account_invalid_request_401)
        balance_after = Account.get_account_by_id(db_session, deposit_account_invalid_request_401.accountId)
        assert balance_before is not None, 'The account must exist in the DB'
        assert balance_before.balance == balance_after.balance, 'The balance should not change with error 400'
