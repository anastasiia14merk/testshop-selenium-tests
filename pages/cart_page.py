from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage

class CartPage(BasePage):
    page_url = 'shop/cart'

    def get_product_name(self):
        wait = WebDriverWait(self.driver, 10)
        product_name = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR,
            'a[href="/shop/customizable-desk-9#attr=1,3"]'))
        )
        return product_name.text.strip()

    def get_product_quantity(self):
        wait = WebDriverWait(self.driver, 10)
        quantity_field = wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, '.o_cart_product[data-product-id="12"] input.js_quantity')
            )
        )
        return int(quantity_field.get_property("value"))

    def increase_products_quantity(self):
        wait = WebDriverWait(self.driver, 10)
        plus_button = wait.until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR,
                    '.o_cart_product[data-product-id="12"] a[aria-label="Add one"]'
                )
            )
        )
        plus_button.click()

    def wait_for_quantity_is_two(self):
        wait = WebDriverWait(self.driver, 10)
        def quantity_is_two(_driver):
            quantity = self.get_product_quantity()
            return quantity == 2

        wait.until(quantity_is_two)

    def remove_product_from_cart(self):
        wait = WebDriverWait(self.driver, 10)
        minus_button = wait.until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR,
                    '.o_cart_product[data-product-id="12"] a[aria-label="Remove one"]'
                )
            )
        )
        minus_button.click()

    def empty_cart_title(self):
        wait = WebDriverWait(self.driver, 10)
        empty_cart_title = wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR,
                 'div.js_cart_lines.alert-info'))
        )
        empty_cart_title = empty_cart_title.text.strip()
        return empty_cart_title
