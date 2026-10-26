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
    assert cart_page.get_product_quantity() == 1


def test_product_quantity_plus_one(cart_with_one_item):
    cart_page = cart_with_one_item
    cart_page.increase_products_quantity()
    cart_page.wait_for_quantity_is_two()
    assert cart_page.get_product_quantity() == 2


def test_product_quantity_minus_one(cart_with_one_item):
    cart_page = cart_with_one_item
    cart_page.remove_product_from_cart()
    assert cart_page.empty_cart_title() == 'Your cart is empty!'




