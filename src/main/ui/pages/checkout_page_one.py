from playwright.sync_api import Page

class CheckoutPageOne():
    URL = 'https://www.saucedemo.com/checkout-step-one.html'

    def __init__(self, page: Page):
        self.page = page
        self.burger_menu_button = page.get_by_role('button', name='Open Menu')
        self.logout_link = page.get_by_role('button', name='Logout')
        self.all_item_link = page.get_by_role('link', name='All Items')
        self.cart_link = page.locator('.shopping_cart_link')
        self.cancel_to_return_cart = page.get_by_role('button', name='Go back Cancel')
        self.button_continue = page.get_by_role('button', name='Continue')
        self.first_name = page.get_by_role('textbox', name='First Name')
        self.last_name = page.get_by_role('textbox', name='Last Name')
        self.zip_postal_code = page.get_by_role('textbox', name='Zip/Postal Code')
        self.error_text = page.locator('.error-message-container')

    def enter_checkout(self, first_name: str, last_name: str, zip_code: str):
        self.first_name.fill(first_name)
        self.last_name.fill(last_name)
        self.zip_postal_code.fill(zip_code)
        self.button_continue.click()

    def open(self):
        self.page.goto(self.URL)

    def logout(self):
        self.burger_menu_button.click()
        self.logout_link.click()

    def catalog(self):
        self.burger_menu_button.click()
        self.all_item_link.click()

    def cancel_to_return(self):
        self.cancel_to_return_cart.click()

    