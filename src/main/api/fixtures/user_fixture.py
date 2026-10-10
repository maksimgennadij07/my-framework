import pytest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.models.credit_request_request import CreditRequestRequest
from src.main.api.models.deposit_account_request import DepositAccountRequest
from src.main.api.models.transfer_account_request import TransferAccountRequest


@pytest.fixture
def create_user_request(api_manager):
    create_user_req = CreateUserRequest(username="T1000", password="Pas!sw0rd", role="ROLE_USER")
    api_manager.admin_steps.create_user(create_user_req)
    return create_user_req

@pytest.fixture
def deposit_account_request(api_manager, create_user_request):
    response = api_manager.user_steps.create_account(create_user_request)
    deposit_account = DepositAccountRequest(accountId=response.id, amount=1000.5)
    return create_user_request, deposit_account

@pytest.fixture
def deposit_account_invalid_request_400(api_manager, create_user_request):
    response = api_manager.user_steps.create_account(create_user_request)
    deposit_account = DepositAccountRequest(accountId=response.id, amount=-1000.5)
    return create_user_request, deposit_account

@pytest.fixture
def deposit_account_invalid_request_401(api_manager, create_user_request):
    response = api_manager.user_steps.create_account(create_user_request)
    deposit_account = DepositAccountRequest(accountId=response.id, amount=1000.5)
    return deposit_account

@pytest.fixture
def transfer_account_request(api_manager, deposit_account_request):
    create_user, deposit_account = deposit_account_request
    acc2 = api_manager.user_steps.create_account(create_user)
    api_manager.user_steps.deposit_account(create_user, deposit_account)
    transfer_account = TransferAccountRequest(
        fromAccountId = deposit_account.accountId,
        toAccountId = acc2.id,
        amount = 500.75
    )
    return create_user, deposit_account, transfer_account

@pytest.fixture
def transfer_account_invalid_request_401(transfer_account_request):
    create_user, deposit_account, transfer_account = transfer_account_request
    return transfer_account

@pytest.fixture
def create_user_request_credit(api_manager):
    create_user = CreateUserRequest(username="T1000", password="Pas!sw0rd", role="ROLE_CREDIT_SECRET")
    api_manager.admin_steps.create_user(create_user)
    response = api_manager.user_steps.create_account(create_user)
    credit_request = CreditRequestRequest(accountId=response.id, amount=5000, termMonths=12)
    return create_user, credit_request

@pytest.fixture
def credit_repay_request(api_manager, create_user_request_credit):
    create_user, credit_request = create_user_request_credit
    response = api_manager.user_steps.credit_request(create_user, credit_request)
    credit_repay = CreditRepayRequest(
        creditId = response.creditId,
        accountId = response.id,
        amount = response.balance
    )
    return create_user, credit_repay, credit_request

@pytest.fixture
def credit_repay_invalid_request_422(credit_repay_request):
    create_user, credit_repay, credit_request = credit_repay_request
    credit_repay.amount = 500
    return create_user, credit_repay, credit_request