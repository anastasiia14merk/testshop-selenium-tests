from selenium import webdriver

import pytest

from pages.cart_page import CartPage
from pages.product_page import ProductPage

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

@pytest.fixture
def cart_with_one_item(driver):
    product_page = ProductPage(driver)
    product_page.open()
    product_page.add_to_cart()
    product_page.continue_shopping()

    cart_page = CartPage(driver)
    cart_page.open()
    assert cart_page.get_product_quantity() == 1
    return cart_page


