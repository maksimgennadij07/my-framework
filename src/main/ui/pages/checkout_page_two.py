from playwright.sync_api import Page


class CheckoutPageTwo():
    URL = 'https://www.saucedemo.com/checkout-step-two.html'

    def __init__(self, page: Page):
        self.page = page
        self.burger_menu_button = page.get_by_role('button', name='Open Menu')
        self.logout_link = page.get_by_role('button', name='Logout')
        self.all_item_link = page.get_by_role('link', name='All Items')
        self.cancel_to_return_step_one = page.get_by_role('button', name='Go back Cancel')
        self.cart_list = page.locator('.cart-list')
        self.cart_item = page.locator('.cart_item')
        self.item_name = page.locator('[data-test="inventory-item-name"]')
        self.item_price = page.locator('[data-test="inventory-item-price"]')
        self.cart_quantity = page.locator('.cart_quantity')
        self.finish_button = page.get_by_role('button', name='Finish')
        self.item_total = page.locator('.summary_subtotal_label')
        self.tax = page.locator('.summary_tax_label')
        self.total = page.locator('.summary_total_label')

    def open(self):
        self.page.goto(self.URL)

    def logout(self):
        self.burger_menu_button.click()
        self.logout_link.click()

    def catalog(self):
        self.burger_menu_button.click()
        self.all_item_link.click()

    def cancel_to_return(self):
        self.cancel_to_return_step_one.click()

    def get_item_total_price_from_checkout(self):
        if self.item_total.text_content() != 'Item total: $0':
            item_total_text = self.item_total.text_content()
            item_total = float(item_total_text.replace('Item total: $', ''))
            return item_total
        return 0

    def get_sum_tax_price_from_checkout(self):
        if self.tax.text_content() != 'Tax: $0.00':
            tax_text = self.tax.text_content()
            tax = float(tax_text.replace('Tax: $', ''))
            return tax
        return 0

    def get_sum_total_price_from_checkout(self):
        if self.total.text_content() != 'Total: $0.00':
            total_text = self.total.text_content()
            total = float(total_text.replace('Total: $', ''))
            return total
        return 0

    def click_finish_button(self):
        self.finish_button.click()