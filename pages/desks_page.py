import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class DesksPage(BasePage):
    page_url = 'shop/category/desks-1'

    PRODUCT_CARDS = (By.CSS_SELECTOR, 'form.oe_product_cart')
    CUSTOMIZABLE_DESK = (
        By.CSS_SELECTOR,
        'a[itemprop="name"][href^="/shop/customizable-desk-9"]',
    )
    CATEGORY_NAME = (By.CSS_SELECTOR, 'ol.breadcrumb li:last-child span')
    LIST_BUTTON = (By.CSS_SELECTOR, 'label[for="o_wsale_apply_list"]')
    LIST_INPUT = (By.ID, 'o_wsale_apply_list')
    PRODUCTS_GRID = (By.ID, 'products_grid')

    @allure.step('Open Customizable Desk from the category')
    def open_customizable_desk(self):
        self.click(self.CUSTOMIZABLE_DESK)
        self.wait.until(EC.url_contains('/shop/customizable-desk-9'))
        self.wait_for_page_ready()

    @allure.step('Read the category name')
    def get_category_name(self):
        return self.wait_for_visible(self.CATEGORY_NAME).text.strip()

    @allure.step('Read names and numeric prices from all product cards')
    def get_products(self):
        def read_products(driver):
            cards = driver.find_elements(*self.PRODUCT_CARDS)
            if not cards or not all(card.is_displayed() for card in cards):
                return False
            return [
                {
                    'name': card.find_element(
                        By.CSS_SELECTOR, 'a[itemprop="name"]'
                    ).text.strip(),
                    'price': self.parse_price(card.find_element(
                        By.CSS_SELECTOR, '.product_price .oe_currency_value'
                    ).text),
                }
                for card in cards
            ]

        return self.wait.until(read_products)

    @allure.step('Read the applied product layout')
    def is_list_view(self):
        grid = self.driver.find_element(*self.PRODUCTS_GRID)
        return 'o_wsale_layout_list' in grid.get_attribute('class').split()

    @allure.step('Switch to list view and wait for the applied layout')
    def switch_to_list_view(self):
        self.click(self.LIST_BUTTON)
        self.wait.until(EC.element_located_to_be_selected(self.LIST_INPUT))
        self.wait.until(
            lambda driver: self.is_list_view(),
            message='The category did not apply the list layout',
        )
