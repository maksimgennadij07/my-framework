import allure
from src.main.ui.pages.checkout_page_one import CheckoutPageOne
from src.main.ui.pages.checkout_page_two import CheckoutPageTwo
from playwright.sync_api import Page, expect


class CheckoutSteps():

    def __init__(self, page: Page):
        self.page = page
        self.checkout_page_one= CheckoutPageOne(page)
        self.checkout_page_two= CheckoutPageTwo(page)

    @allure.step('Filling in the input fields on the checkout-step-one page')
    def enter_checkout(self, first_name: str, last_name: str, zip_code: str):
        self.checkout_page_one.enter_checkout(first_name, last_name, zip_code)
        return self

    @allure.step('Calculating the Item Total on the checkout-step-two page')
    def get_item_total_price_from_checkout(self):
        item_total = self.checkout_page_two.get_item_total_price_from_checkout()
        return item_total

    @allure.step('Calculating the Tax Total on the Checkout-Step-Two Page')
    def get_sum_tax_price_from_checkout(self):
        tax = self.checkout_page_two.get_sum_tax_price_from_checkout()
        return tax

    @allure.step('Calculating the Total Product Sum on the Checkout-Step-Two Page')
    def get_sum_total_price_from_checkout(self):
        total = self.checkout_page_two.get_sum_total_price_from_checkout()
        return total

    @allure.step('Click the Finish button.')
    def click_finish_button(self):
        self.checkout_page_two.click_finish_button()
        return self

    @allure.step('"We receive an error message if one exists."')
    def get_error_text(self):
        if self.checkout_page_one.error_text.is_visible():
            return self.checkout_page_one.error_text.inner_text()
        return ''
