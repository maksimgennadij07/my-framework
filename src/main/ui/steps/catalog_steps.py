import allure
from src.main.ui.pages.login_page import LoginPage
from src.main.ui.pages.catalog_page import CatalogPage
from playwright.sync_api import Page, expect


class CatalogSteps:

    def __init__(self, page: Page):
        self.page = page
        self.catalog_page = CatalogPage(page)

    @allure.step('Open catalog page')
    def open_catalog_page(self):
        self.catalog_page.open()
        expect(self.page).to_have_url(CatalogPage.URL)
        return self

    @allure.step('We log out and check the correctness of the redirect.')
    def logout(self):
        self.catalog_page.logout()
        expect(self.page).to_have_url(LoginPage.URL)
        expect(self.page.locator('#login-button')).to_be_visible()
        return self

    @allure.step('sort products by the entered filter {option}')
    def sort_items(self, option: str):
        self.catalog_page.sort_catalog_items(option)
        return self

    @allure.step('Go to the cart page')
    def open_cart(self):
        self.catalog_page.open_cart()
        return self

    @allure.step('add the product {product_name} to the cart')
    def add_to_cart(self, product_name: str):
        button = self.catalog_page.add_to_cart(product_name)
        return button

    @allure.step('remove the item {product_name} to the cart')
    def remove_from_cart(self, product_name: str):
        button = self.catalog_page.remove_from_cart(product_name)
        return button

    @allure.step('we get the number of items in the basket')
    def get_cart_count(self):
        return self.catalog_page.get_cart_count()

    @allure.step('we get the counter of products in the cart')
    def cart_badge(self):
        return self.catalog_page.cart_badge()

    @allure.step('we get the number of product cards')
    def get_product_count(self) -> int:
        return self.catalog_page.get_products_count()

    @allure.step('we get a list of product names')
    def get_product_names(self) -> list[str]:
        return self.catalog_page.get_product_names()

    @allure.step('we get a list of product prices')
    def get_product_prices(self) -> list[float]:
        return self.catalog_page.get_product_prices()

    @allure.step('open the product details page {product_name}')
    def open_product_details(self, product_name: str):
        return self.catalog_page.open_product_details(product_name)