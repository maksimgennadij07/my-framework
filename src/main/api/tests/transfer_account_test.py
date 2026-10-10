import pytest
from sqlalchemy.orm import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.models.account_table import Account
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.db.crud.transaction_crud import TransactionCrudDb as Transaction


@pytest.mark.api
class TestTransferMoney:
    # Позитивный сценарий перевода между счетами
    def test_transfer_money_valid(self,api_manager: ApiManager, transfer_account_request, db_session: Session):
        create_user, deposit_account, transfer_account = transfer_account_request
        response = api_manager.user_steps.transfer_account(create_user, transfer_account)
        result = deposit_account.amount - transfer_account.amount
        assert transfer_account.fromAccountId == response.fromAccountId
        assert transfer_account.toAccountId == response.toAccountId
        assert response.fromAccountIdBalance == result

        account_from_db = Account.get_account_by_id(db_session, deposit_account.accountId)
        assert account_from_db.balance == result

        transaction_from_db_one = Transaction.get_transction_by_from_account_id(db_session, transfer_account.fromAccountId)
        assert transaction_from_db_one.from_account_id == transfer_account.fromAccountId

        transaction_from_db_two = Transaction.get_transction_by_to_account_id(db_session, transfer_account.toAccountId)
        assert transaction_from_db_two.to_account_id == transfer_account.toAccountId

    # Негативная проверка - отсутствует токен авторизации при переводе - ОР 401
    def test_transfer_money_invalid(self, api_manager: ApiManager, transfer_account_invalid_request_401, db_session: Session):
        api_manager.user_steps.transfer_account_invalid_401(transfer_account_invalid_request_401)

        account_from_db = Account.get_account_by_id(db_session, transfer_account_invalid_request_401.toAccountId)
        assert account_from_db.balance == 0

        transaction_from_db_one = Transaction.get_transction_by_from_account_id(db_session, transfer_account_invalid_request_401.toAccountId)
        assert transaction_from_db_one is None