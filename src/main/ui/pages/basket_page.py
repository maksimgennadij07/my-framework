from playwright.sync_api import Page


class BasketPage():
    URL = 'https://www.saucedemo.com/cart.html'

    def __init__(self, page: Page):
        self.page = page
        self.burger_menu_button = page.get_by_role('button', name='Open Menu')
        self.logout_link = page.get_by_role('button', name='Logout')
        self.all_item_link = page.get_by_role('link', name='All Items')

        self.cart_list = page.locator('.cart-list')
        self.cart_item = page.locator('.cart_item')
        self.item_name = page.locator('[data-test="inventory-item-name"]')
        self.item_price = page.locator('[data-test="inventory-item-price"]')
        self.checkout_button = page.get_by_role('button', name='Checkout')
        self.cart_quantity = page.locator('.cart_quantity')

    def open(self):
        self.page.goto(self.URL)

    def logout(self):
        self.burger_menu_button.click()
        self.logout_link.click()

    def catalog(self):
        self.burger_menu_button.click()
        self.all_item_link.click()

    def get_count_items_in_cart(self):
        if self.cart_quantity.all_inner_texts() is not None:
            count_items_text = self.cart_quantity.all_text_contents()
            count_items = [int(qty) for qty in count_items_text]
            return sum(count_items)
        return 0

    def get_item_name(self, product_name: str):
        return self.item_name.filter(has_text=product_name)

    def get_all_cart_items(self):
        return self.item_name.all_inner_texts()

    def remove_item_from_cart(self, product_name: str):
        card = self.cart_item.filter(has_text=product_name)
        button = card.get_by_role('button', name='Remove')
        button.click()
        return button

    def get_sum_all_price_items_from_cart(self):
        if self.cart_item.all_inner_texts() is not None:
            price_text = self.item_price.all_text_contents()
            price = [float(p.replace('$', '')) for p in price_text]
            return sum(price)
        return 0

    def open_checkout(self):
        self.checkout_button.click()