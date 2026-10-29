import allure
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CartPage(BasePage):
    page_url = "shop/cart"
    PRODUCT_ROWS = (By.CSS_SELECTOR, ".o_cart_product")
    PRODUCT_NAME = (By.CSS_SELECTOR, "h6")
    QUANTITY = (By.CSS_SELECTOR, "input.js_quantity")
    LINE_TOTAL = (
        By.CSS_SELECTOR,
        '[name="website_sale_cart_line_price"] .oe_currency_value',
    )

    def _find_product_row(self, product_name):
        for row in self.driver.find_elements(*self.PRODUCT_ROWS):
            if not row.is_displayed():
                continue
            name = row.find_element(*self.PRODUCT_NAME).text.strip()
            if name == product_name:
                return row
        raise NoSuchElementException(f"Cart does not contain {product_name!r}")

    @allure.step("Read product names from a nonempty cart")
    def get_product_names(self):
        def read_names(driver):
            names = []
            for row in driver.find_elements(*self.PRODUCT_ROWS):
                if row.is_displayed():
                    name = row.find_element(*self.PRODUCT_NAME).text.strip()
                    names.append(name)
            return names

        return self.wait.until(read_names)

    @allure.step("Wait for {product_name} to disappear from the cart")
    def wait_for_product_removed(self, product_name):
        self.wait.until(
            lambda driver: all(
                row.find_element(*self.PRODUCT_NAME).text.strip() != product_name
                for row in driver.find_elements(*self.PRODUCT_ROWS)
            ),
            message=f"Cart still contains {product_name!r}",
        )

    @allure.step("Read the name of {product_name}")
    def get_product_name(self, product_name):
        def read_name(driver):
            row = self._find_product_row(product_name)
            return row.find_element(*self.PRODUCT_NAME).text.strip()

        return self.wait.until(read_name)

    @allure.step("Read the cart quantity of {product_name}")
    def get_product_quantity(self, product_name):
        def read_quantity(driver):
            row = self._find_product_row(product_name)
            return row.find_element(*self.QUANTITY).get_property("value")

        return int(self.wait.until(read_quantity))

    @allure.step("Read the line total of {product_name}")
    def get_total_price(self, product_name):
        def read_price(driver):
            row = self._find_product_row(product_name)
            return row.find_element(*self.LINE_TOTAL).text.strip()

        return self.parse_price(self.wait.until(read_price))

    def _change_quantity(self, product_name, button_label):
        self.wait_for_page_ready()

        def click_button(driver):
            button = self._find_product_row(product_name).find_element(
                By.CSS_SELECTOR, f'a[aria-label="{button_label}"]'
            )
            if not button.is_displayed() or not button.is_enabled():
                return False
            button.click()
            return True

        self.wait.until(click_button, message=f"Could not change quantity of {product_name!r}")

    @allure.step("Increase the cart quantity of {product_name} by one")
    def increase_products_quantity(self, product_name):
        self._change_quantity(product_name, "Add one")

    @allure.step("Wait for {product_name} quantity to become {expected_quantity}")
    def wait_for_quantity(self, expected_quantity, product_name):
        def quantity_matches(driver):
            row = self._find_product_row(product_name)
            return int(row.find_element(*self.QUANTITY).get_property("value")) == expected_quantity

        self.wait.until(
            quantity_matches,
            message=f"Quantity of {product_name!r} did not become {expected_quantity}",
        )

    @allure.step("Wait for {product_name} line total to become {expected_total}")
    def wait_for_product_total(self, expected_total, product_name):
        def total_matches(driver):
            row = self._find_product_row(product_name)
            return self.parse_price(row.find_element(*self.LINE_TOTAL).text) == expected_total

        self.wait.until(
            total_matches,
            message=f"Line total of {product_name!r} did not become {expected_total}",
        )

    @allure.step("Decrease the cart quantity of {product_name} by one")
    def remove_product_from_cart(self, product_name):
        self._change_quantity(product_name, "Remove one")

    @allure.step("Read the empty-cart message")
    def empty_cart_title(self):
        return self.read_text((By.CSS_SELECTOR, "div.js_cart_lines.alert-info"))
