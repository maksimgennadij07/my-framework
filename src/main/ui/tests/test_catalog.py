from playwright.sync_api import expect
from src.main.ui.pages.catalog_page import CatalogPage
from src.main.ui.steps.catalog_steps import CatalogSteps


class TestCatalog:
    def test_catalog_count_product(self, auth_page):
        catalog_steps = CatalogSteps(auth_page)
        expect(auth_page).to_have_url(CatalogPage.URL)
        count_item = catalog_steps.get_product_count()
        assert count_item == 6

    def test_sorted_by_name_a_z(self, auth_page):
        catalog_steps = CatalogSteps(auth_page)
        expect(auth_page).to_have_url(CatalogPage.URL)
        names = catalog_steps.sort_items('az').get_product_names()
        assert names == sorted(names), 'Products are not sorted by name A-Z'

    def test_sorted_by_name_z_a(self, auth_page):
        catalog_steps = CatalogSteps(auth_page)
        expect(auth_page).to_have_url(CatalogPage.URL)
        names = catalog_steps.sort_items('za').get_product_names()
        assert names == sorted(names, reverse=True), 'Products are not sorted by name Z-A'

    def test_sort_by_price_low_high(self, auth_page):
        catalog_steps = CatalogSteps(auth_page)
        expect(auth_page).to_have_url(CatalogPage.URL)
        prices = catalog_steps.sort_items('lohi').get_product_prices()
        assert prices == sorted(prices), 'Products are not sorted by price low-high'

    def test_sort_by_price_high_low(self, auth_page):
        catalog_steps = CatalogSteps(auth_page)
        expect(auth_page).to_have_url(CatalogPage.URL)
        prices = catalog_steps.sort_items('hilo').get_product_prices()
        assert prices == sorted(prices, reverse=True), 'Products are not sorted by price high-low'

    def test_add_to_cart(self, auth_page):
        catalog_steps = CatalogSteps(auth_page)
        add_button = catalog_steps.add_to_cart('Sauce Labs Onesie')
        expect(add_button).to_have_text('Remove')
        assert catalog_steps.get_cart_count() == 1

    def test_add_to_cart_and_remove(self, auth_page):
        catalog_steps = CatalogSteps(auth_page)
        add_button = catalog_steps.add_to_cart('Sauce Labs Onesie')
        expect(add_button).to_have_text('Remove')
        assert catalog_steps.get_cart_count() == 1
        remove_button = catalog_steps.remove_from_cart('Sauce Labs Onesie')
        expect(remove_button).to_have_text('Add to cart')
        assert catalog_steps.get_cart_count() == 0

    def test_product_details_onesie(self, auth_page):
        catalog_steps = CatalogSteps(auth_page)
        name, price, detail_name, detail_price = catalog_steps.open_product_details('Sauce Labs Onesie')

        assert name == detail_name, 'the product name does not match'
        assert price == detail_price, 'the price of the product does not match'

    def test_product_details_jacket(self, auth_page):
        catalog_steps = CatalogSteps(auth_page)
        name, price, detail_name, detail_price = catalog_steps.open_product_details('Sauce Labs Fleece Jacket')

        assert name == detail_name, 'the product name does not match'
        assert price == detail_price, 'the price of the product does not match'