import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class ProductPage(BasePage):
    page_url = "shop/customizable-desk-9#attr=1,3"
    ADD_TO_CART = (By.ID, "add_to_cart")
    ALUMINIUM = (By.CSS_SELECTOR, '.js_main_product input[data-value_name="Aluminium"]')
    PRODUCT_ID = (By.CSS_SELECTOR, ".js_main_product input.product_id")
    QUANTITY = (By.CSS_SELECTOR, '.js_main_product input[name="add_qty"]')
    CONFIGURATOR = (By.CSS_SELECTOR, ".modal.show .oe_advanced_configurator_modal")
    CONTINUE_SHOPPING = (
        By.CSS_SELECTOR,
        ".modal.show:has(.oe_advanced_configurator_modal) button.btn-secondary",
    )

    @allure.step("Add the product to the cart and wait for its options dialog")
    def add_to_cart(self):
        self.click(self.ADD_TO_CART)
        self.wait_for_visible(self.CONFIGURATOR)

    @allure.step("Close the options dialog and continue shopping")
    def continue_shopping(self):
        self.click(self.CONTINUE_SHOPPING)
        self.wait.until(EC.invisibility_of_element_located(self.CONFIGURATOR))

    @allure.step("Wait for {expected_quantity} units in the cart")
    def wait_for_cart_quantity(self, expected_quantity):
        def quantity_matches(driver):
            counters = driver.find_elements(By.CSS_SELECTOR, ".my_cart_quantity")
            visible = [counter for counter in counters if counter.is_displayed()]
            return bool(visible) and all(
                counter.text.strip() == str(expected_quantity) for counter in visible
            )

        self.wait.until(quantity_matches, message=f"Cart counter did not become {expected_quantity}")

    @allure.step("Read the product name")
    def get_product_name(self):
        return self.read_text((By.CSS_SELECTOR, 'h1[itemprop="name"]'))

    @allure.step("Read the selected product price")
    def get_price(self):
        price_locator = (By.CSS_SELECTOR, ".js_main_product .oe_price .oe_currency_value")
        return self.parse_price(self.read_text(price_locator))

    @allure.step("Select Aluminium legs and wait for the variant update")
    def select_aluminium(self):
        self.wait_for_page_ready()
        if self.is_aluminium_selected():
            return
        previous_id = self.driver.find_element(*self.PRODUCT_ID).get_property("value")
        self.click(self.ALUMINIUM)
        def variant_updated(driver):
            aluminium = driver.find_element(*self.ALUMINIUM)
            product_id = driver.find_element(*self.PRODUCT_ID).get_property("value")
            return aluminium.is_selected() and product_id not in ("", "0", previous_id)

        self.wait.until(
            variant_updated,
            message="Aluminium was selected but its product variant did not update",
        )

    @allure.step("Read the Aluminium radio-button state")
    def is_aluminium_selected(self):
        aluminium = self.wait_for_visible(self.ALUMINIUM)
        return aluminium.is_selected()

    @allure.step("Increase the product-page quantity by one")
    def increase_quantity(self):
        self.click((By.CSS_SELECTOR, '.js_main_product a[aria-label="Add one"]'))

    @allure.step("Read the product-page quantity")
    def get_quantity(self):
        def read_quantity(driver):
            field = driver.find_element(*self.QUANTITY)
            return field.get_property("value")

        return int(self.wait.until(read_quantity))

    @allure.step("Wait for product-page quantity to become {expected_quantity}")
    def wait_for_quantity(self, expected_quantity):
        def quantity_matches(driver):
            field = driver.find_element(*self.QUANTITY)
            return int(field.get_property("value")) == expected_quantity

        self.wait.until(
            quantity_matches,
            message=f"Product-page quantity did not become {expected_quantity}",
        )
