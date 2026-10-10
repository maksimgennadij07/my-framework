import pytest
from sqlalchemy.orm import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.credit_crud import CreditCrudDb as Credit


@pytest.mark.api
class TestCreditRepay:
    # Позитивная проверка на погашение кредита
    def test_credit_repay_valid(self, api_manager: ApiManager, credit_repay_request, db_session: Session):
        create_user, credit_repay, credit_request = credit_repay_request
        response = api_manager.user_steps.credit_repay(create_user, credit_repay)
        assert credit_repay.creditId == response.creditId
        assert credit_repay.amount == response.amountDeposited

        credit_from_db = Credit.get_credit_by_account_id(db_session, credit_repay.accountId)
        assert credit_from_db.account_id == credit_repay.accountId
        assert credit_from_db.amount == credit_repay.amount
        assert credit_from_db.term_months == credit_request.termMonths
        assert credit_from_db.balance == 0


# Негативная проверка на погашение кредита(недостаточно деняк) - ОР 422
    def test_credit_repay_invalid(self, api_manager: ApiManager, credit_repay_invalid_request_422, db_session: Session):
        create_user, credit_repay, credit_request = credit_repay_invalid_request_422
        api_manager.user_steps.credit_repay_invalid_422(create_user, credit_repay)

        credit_from_db = Credit.get_credit_by_account_id(db_session, credit_request.accountId)
        assert credit_from_db.account_id == credit_request.accountId
        assert credit_from_db.amount == credit_request.amount
        assert credit_from_db.term_months == credit_request.termMonths
        assert credit_from_db.balance == -credit_request.amount