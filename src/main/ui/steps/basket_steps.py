import allure
from src.main.ui.pages.basket_page import BasketPage
from playwright.sync_api import Page, expect


class BasketSteps:

    def __init__(self, page: Page):
        self.page = page
        self.basket_page = BasketPage(page)

    @allure.step('Open basket page')
    def open_basket_page(self):
        self.basket_page.open()
        expect(self.page).to_have_url(BasketPage.URL)
        return self

    @allure.step('we receive the goods from the basket {product_name}')
    def get_item_name(self, product_name):
        return self.basket_page.get_item_name(product_name)

    @allure.step('we get all the goods from the cart')
    def get_all_cart_items(self):
        return self.basket_page.get_all_cart_items()

    @allure.step('remove the item {product_name} from the cart')
    def remove_item_from_cart(self, product_name):
        return self.basket_page.remove_item_from_cart(product_name)

    @allure.step('We calculate the total amount of all items in the basket.')
    def get_sum_all_price_items_from_cart(self):
        return self.basket_page.get_sum_all_price_items_from_cart()

    @allure.step('go to page Checkout')
    def open_checkout(self):
        self.basket_page.open_checkout()
        return self