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