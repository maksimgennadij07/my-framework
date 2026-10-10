import allure
from src.main.ui.pages.login_page import LoginPage
from playwright.sync_api import Page, expect


class LoginSteps:

    def __init__(self, page: Page):
        self.page = page
        self.login_page = LoginPage(page)

    @allure.step('Open the login page')
    def open_login_page(self):
        self.login_page.open()
        expect(self.page).to_have_url('https://www.saucedemo.com/')
        return self

    @allure.step('log in as user {username}')
    def login(self, username: str, password: str):
        self.login_page.login(username, password)
        return self

    @allure.step('We receive an error text when logging in.')
    def get_error_text(self) -> str:
        return self.login_page.get_error_text()