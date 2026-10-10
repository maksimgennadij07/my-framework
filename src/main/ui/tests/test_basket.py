from playwright.sync_api import expect
from src.main.ui.pages.catalog_page import CatalogPage
from src.main.ui.steps.catalog_steps import CatalogSteps
from src.main.ui.steps.basket_steps import BasketSteps


class TestBasket:
    def test_add_item_and_check_in_cart(self, auth_page):
        catalog_steps = CatalogSteps(auth_page)
        basket_steps = BasketSteps(auth_page)
        expect(auth_page).to_have_url(CatalogPage.URL)
        catalog_steps.add_to_cart('Sauce Labs Backpack')
        catalog_steps.open_cart()
        item_name = basket_steps.get_item_name('Sauce Labs Backpack')
        assert item_name.inner_text() == 'Sauce Labs Backpack'

    def test_add_two_item_and_check_in_cart(self, auth_page):
        catalog_steps = CatalogSteps(auth_page)
        basket_steps = BasketSteps(auth_page)
        expect(auth_page).to_have_url(CatalogPage.URL)
        catalog_steps.add_to_cart('Sauce Labs Fleece Jacket')
        catalog_steps.add_to_cart('Sauce Labs Bolt T-Shirt')
        catalog_steps.open_cart()
        item_names = basket_steps.get_all_cart_items()
        assert 'Sauce Labs Fleece Jacket' in item_names
        assert 'Sauce Labs Bolt T-Shirt' in item_names

    def test_remove_item_from_cart(self, auth_page):
        catalog_steps = CatalogSteps(auth_page)
        basket_steps = BasketSteps(auth_page)
        expect(auth_page).to_have_url(CatalogPage.URL)
        catalog_steps.add_to_cart('Sauce Labs Fleece Jacket')
        catalog_steps.open_cart()
        item_name = basket_steps.get_item_name('Sauce Labs Fleece Jacket')
        assert item_name.inner_text() == 'Sauce Labs Fleece Jacket'
        basket_steps.remove_item_from_cart('Sauce Labs Fleece Jacket')
        expect(item_name).not_to_be_visible()

    def test_remove_two_item_from_cart(self, auth_page):
        catalog_steps = CatalogSteps(auth_page)
        basket_steps = BasketSteps(auth_page)
        expect(auth_page).to_have_url(CatalogPage.URL)
        catalog_steps.add_to_cart('Sauce Labs Backpack')
        catalog_steps.add_to_cart('Test.allTheThings() T-Shirt (Red)')
        catalog_steps.open_cart()
        backpack = basket_steps.get_item_name('Sauce Labs Backpack')
        expect(backpack).to_be_visible()
        shirt = basket_steps.get_item_name('Test.allTheThings() T-Shirt (Red)')
        expect(shirt).to_be_visible()
        basket_steps.remove_item_from_cart('Sauce Labs Backpack')
        basket_steps.remove_item_from_cart('Test.allTheThings() T-Shirt (Red)')
        expect(backpack).not_to_be_visible()
        expect(shirt).not_to_be_visible()