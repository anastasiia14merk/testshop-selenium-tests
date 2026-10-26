from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage

class DesksPage(BasePage):
    page_url = 'shop/category/desks-1'

    def open_customizable_desk(self):
        wait = WebDriverWait(self.driver, 10)
        customizable_desk = wait.until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR,
                    'a[itemprop="name"][href="/shop/customizable-desk-9?category=1"]'
                )
            )
        )
        customizable_desk.click()

