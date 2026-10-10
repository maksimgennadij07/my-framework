from src.main.api.foundation.endpoint import Endpoint
from src.main.api.foundation.requesters.validate_crud_requester import ValidateCrudRequester
from src.main.api.foundation.requesters.crud_requester import CrudRequester
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.models.credit_request_request import CreditRequestRequest
from src.main.api.models.deposit_account_request import DepositAccountRequest
from src.main.api.models.transfer_account_request import TransferAccountRequest
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.steps.base_steps import BaseSteps


class UserSteps(BaseSteps):
    def create_account(self, create_user_request: CreateUserRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.CREATE_ACCOUNT,
            ResponseSpecs.status_code_201()
        ).post()
        return response

    def create_account_invalid_403(self):
        CrudRequester(
            RequestSpecs.auth_headers(username='admin', password='123456'),
            Endpoint.CREATE_ACCOUNT,
            ResponseSpecs.status_code_403()
        ).post()

    def deposit_account(self, create_user_request: CreateUserRequest, deposit_account_request: DepositAccountRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.DEPOSIT_ACCOUNT,
            ResponseSpecs.status_code_200()
        ).post(deposit_account_request)
        return response

    def deposit_account_invalid_400(self, create_user_request: CreateUserRequest, deposit_account_request: DepositAccountRequest):
        CrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.DEPOSIT_ACCOUNT,
            ResponseSpecs.status_code_400()
        ).post(deposit_account_request)

    def deposit_account_invalid_401(self, deposit_account_request: DepositAccountRequest):
        CrudRequester(
            RequestSpecs.no_auth_headers(),
            Endpoint.DEPOSIT_ACCOUNT,
            ResponseSpecs.status_code_401()
        ).post(deposit_account_request)

    def transfer_account(self, create_user_request: CreateUserRequest, transfer_account_request: TransferAccountRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.TRANSFER_ACCOUNT,
            ResponseSpecs.status_code_200()
        ).post(transfer_account_request)
        return response

    def transfer_account_invalid_401(self, transfer_account_request: TransferAccountRequest):
        CrudRequester(
            RequestSpecs.no_auth_headers(),
            Endpoint.TRANSFER_ACCOUNT,
            ResponseSpecs.status_code_401()
        ).post(transfer_account_request)

    def credit_request(self, create_user_request: CreateUserRequest, create_user_request_credit: CreditRequestRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.CREDIT_REQUEST,
            ResponseSpecs.status_code_201()
        ).post(create_user_request_credit)
        return response

    def credit_invalid_request_404(self, create_user_request: CreateUserRequest, credit_request: CreditRequestRequest):
        CrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.CREDIT_REQUEST,
            ResponseSpecs.status_code_404()
        ).post(credit_request)

    def credit_repay(self, create_user_request: CreateUserRequest, credit_repay_request: CreditRepayRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.CREDIT_REPAY,
            ResponseSpecs.status_code_200()
        ).post(credit_repay_request)
        return response

    def credit_repay_invalid_422(self, create_user_request: CreateUserRequest, credit_repay_request: CreditRepayRequest):
        CrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.CREDIT_REPAY,
            ResponseSpecs.status_code_422()
        ).post(credit_repay_request)