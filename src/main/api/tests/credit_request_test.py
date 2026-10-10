import pytest
from sqlalchemy.orm import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.credit_crud import CreditCrudDb as Credit

@pytest.mark.api
class TestCreditRequest:
    # Позитивная проверка на получение кредита
    def test_credit_request_valid(self,api_manager: ApiManager, create_user_request_credit, db_session: Session):
        create_user, credit_request = create_user_request_credit
        response = api_manager.user_steps.credit_request(create_user, credit_request)
        assert credit_request.accountId == response.id
        assert credit_request.amount == response.amount
        assert  credit_request.termMonths == response.termMonths

        credit_from_db = Credit.get_credit_by_account_id(db_session, credit_request.accountId)
        assert credit_from_db.account_id == credit_request.accountId
        assert credit_from_db.amount == credit_request.amount
        assert credit_from_db.term_months == credit_request.termMonths
        assert credit_from_db.balance == -response.balance

    # Негативная проверка на получение кредита
    def test_credit_request_invalid(self,api_manager: ApiManager, create_user_request_credit, db_session: Session):
        create_user, credit_request = create_user_request_credit
        api_manager.user_steps.credit_request(create_user, credit_request)
        api_manager.user_steps.credit_invalid_request_404(create_user, credit_request)

        credit_from_db = Credit.get_credit_by_account_id_all(db_session, credit_request.accountId)
        assert len(credit_from_db) == 1