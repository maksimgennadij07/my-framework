from playwright.sync_api import expect
from src.main.ui.pages.checkout_page_one import CheckoutPageOne
from src.main.ui.pages.checkout_page_two import CheckoutPageTwo
from src.main.ui.steps.catalog_steps import CatalogSteps
from src.main.ui.steps.basket_steps import BasketSteps
from src.main.ui.steps.checkout_steps import CheckoutSteps

class TestCheckoutCart:
    def test_checkout_cart(self, auth_page):
        catalog_steps = CatalogSteps(auth_page)
        basket_steps = BasketSteps(auth_page)
        checkout_steps = CheckoutSteps(auth_page)
        catalog_steps.add_to_cart('Sauce Labs Fleece Jacket')
        catalog_steps.add_to_cart('Sauce Labs Bolt T-Shirt')
        catalog_steps.open_cart()
        item_names = basket_steps.get_all_cart_items()
        assert 'Sauce Labs Fleece Jacket' in item_names
        assert 'Sauce Labs Bolt T-Shirt' in item_names
        prices_sum = basket_steps.get_sum_all_price_items_from_cart()
        basket_steps.open_checkout()
        expect(auth_page).to_have_url(CheckoutPageOne.URL)
        checkout_steps.enter_checkout('Test', 'Test', '232323')
        expect(auth_page).to_have_url(CheckoutPageTwo.URL)
        item_total = checkout_steps.get_item_total_price_from_checkout()
        tax = checkout_steps.get_sum_tax_price_from_checkout()
        total = checkout_steps.get_sum_total_price_from_checkout()
        assert prices_sum == item_total, 'Item total is not equal to prices sum'
        assert prices_sum + tax == total, 'Item total is not equal to prices sum and tax'
        checkout_steps.click_finish_button()
        expect(auth_page).to_have_url('https://www.saucedemo.com/checkout-complete.html')
        thank_text = auth_page.locator('.complete-header', has_text='Thank you for your order!')
        expect(thank_text).to_be_visible()


    def test_checkout_invalid_last_name(self, auth_page):
        catalog_steps = CatalogSteps(auth_page)
        basket_steps = BasketSteps(auth_page)
        checkout_steps = CheckoutSteps(auth_page)
        catalog_steps.add_to_cart('Sauce Labs Fleece Jacket')
        catalog_steps.open_cart()
        item_name = basket_steps.get_item_name('Sauce Labs Fleece Jacket')
        expect(item_name).to_be_visible()
        basket_steps.open_checkout()
        expect(auth_page).to_have_url(CheckoutPageOne.URL)
        checkout_steps.enter_checkout('Test', '', '232323')
        assert "Error: Last Name is required" in checkout_steps.get_error_text()