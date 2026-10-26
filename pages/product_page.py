from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage

class ProductPage(BasePage):
    page_url = 'shop/customizable-desk-9#attr=1,3'

    def add_to_cart(self):
        wait = WebDriverWait(self.driver, 10)
        add_button = wait.until(
            EC.element_to_be_clickable((By.ID, "add_to_cart"))
        )
        add_button.click()

    def continue_shopping(self):
        wait = WebDriverWait(self.driver, 10)
        continue_shopping_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#modal_5 button.btn-secondary'))
        )
        continue_shopping_button.click()
        wait.until(
            EC.invisibility_of_element_located((By.ID, "modal_5"))
        )
        wait.until(self.cart_has_one_item)

    def cart_has_one_item(self, driver):
        counters = driver.find_elements(By.CSS_SELECTOR, ".my_cart_quantity")
        for counter in counters:
            if counter.text.strip() == "1":
                return True
        return False

    def get_product_name(self):
        wait = WebDriverWait(self.driver, 10)
        product_name = wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, 'h1[itemprop="name"]')
            )
        )
        return product_name.text.strip()

