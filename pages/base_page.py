from decimal import Decimal

import allure
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import config


class BasePage:
    page_url = None

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(
            driver,
            config.WAIT_TIMEOUT,
            ignored_exceptions=(StaleElementReferenceException,),
        )

    @allure.step("Open the page")
    def open(self):
        if self.page_url is None:
            raise NotImplementedError("This page has no navigation URL")
        self.driver.get(f"{config.BASE_URL.rstrip('/')}/{self.page_url}")
        self.wait_for_page_ready()

    @allure.step("Wait for the TestShop application to be ready")
    def wait_for_page_ready(self):
        # Сначала ждём загрузки модуля магазина, затем — окончания его запуска.
        self.wait.until(lambda driver: driver.execute_script(
            "return Boolean(window.odoo?.loader?.modules?.get('root.widget'));"
        ))
        self.driver.set_script_timeout(config.WAIT_TIMEOUT)
        error = self.driver.execute_async_script("""
            const done = arguments[0];
            const shop = window.odoo.loader.modules.get('root.widget');
            shop.then(() => done(null), error => done(String(error)));
        """)
        if error:
            raise RuntimeError(f"TestShop startup failed: {error}")

    def wait_for_visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def read_text(self, locator):
        return self.wait_for_visible(locator).text.strip()

    def click(self, locator):
        self.wait_for_page_ready()
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()

    @staticmethod
    def parse_price(text):
        # В магазине запятая отделяет тысячи: "1,500.00" -> Decimal("1500.00").
        return Decimal(text.replace(",", "").replace("\u00a0", "").strip())
