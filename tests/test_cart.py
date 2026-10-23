import pytest

from pages.base_page import BasePage
from pages.cart_page import CartPage
from pages.product_page import ProductPage

def test_add_to_cart(driver):
    product_page = ProductPage(driver)
    product_page.open()
    product_page.add_to_cart()
    product_page.continue_shopping()
    cart_page = CartPage(driver)
    cart_page.open()
    assert cart_page.get_product_name() == 'Customizable Desk (Steel, White)'


