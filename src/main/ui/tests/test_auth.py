from playwright.sync_api import  expect
from src.main.ui.pages.catalog_page import CatalogPage
from src.main.ui.steps.login_steps import LoginSteps
from src.main.ui.steps.catalog_steps import CatalogSteps


class TestAuth:
    def test_auth_logout_standard_user(self, page):
        login_steps = LoginSteps(page)
        catalog_steps = CatalogSteps(page)
        login_steps.open_login_page().login("standard_user", "secret_sauce")
        expect(page).to_have_url(CatalogPage.URL)
        catalog_steps.logout()

    def test_auth_logout_visual_user(self, page):
        login_steps = LoginSteps(page)
        catalog_steps = CatalogSteps(page)
        login_steps.open_login_page().login("visual_user", "secret_sauce")
        expect(page).to_have_url(CatalogPage.URL)
        catalog_steps.logout()

    def test_auth_logout_locked_out_user(self, page):
        login_steps = LoginSteps(page)
        error_text = login_steps.open_login_page().login("locked_out_user", "secret_sauce").get_error_text()
        assert 'locked out' in error_text, 'We are waiting for a message about a blocked user.'