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
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#modal_5 button.btn-secondary.'))
        )
        continue_shopping_button.click()
