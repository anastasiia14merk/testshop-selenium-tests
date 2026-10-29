import allure

from data import ALUMINIUM_WHITE, STEEL_WHITE
from pages.cart_page import CartPage
from pages.product_page import ProductPage


@allure.epic("TestShop UI")
@allure.feature("Shopping cart")
@allure.title("Add a product to the cart")
@allure.description("Add the Steel, White desk and verify its name and quantity.")
def test_add_to_cart(driver):
    product_page = ProductPage(driver)
    product_page.open()
    product_page.add_to_cart()
    product_page.continue_shopping()
    product_page.wait_for_cart_quantity(1)
    cart_page = CartPage(driver)
    cart_page.open()
    with allure.step("Verify the product and its quantity"):
        assert cart_page.get_product_name(STEEL_WHITE) == STEEL_WHITE
        assert cart_page.get_product_quantity(STEEL_WHITE) == 1


@allure.epic("TestShop UI")
@allure.feature("Shopping cart")
@allure.title("Increase cart quantity and recalculate the line total")
@allure.description("Increase quantity from one to two and verify that the line total doubles.")
def test_product_quantity_plus_one(cart_with_one_item):
    cart_page = cart_with_one_item
    initial_total_price = cart_page.get_total_price(STEEL_WHITE)
    cart_page.increase_products_quantity(STEEL_WHITE)
    cart_page.wait_for_quantity(2, STEEL_WHITE)
    cart_page.wait_for_product_total(initial_total_price * 2, STEEL_WHITE)
    with allure.step("Verify the updated quantity and price"):
        assert cart_page.get_product_quantity(STEEL_WHITE) == 2
        assert cart_page.get_total_price(STEEL_WHITE) == initial_total_price * 2


@allure.epic("TestShop UI")
@allure.feature("Shopping cart")
@allure.title("Remove the last item from the cart")
@allure.description("Decrease the only item quantity to zero and verify the empty-cart message.")
def test_product_quantity_minus_one(cart_with_one_item):
    cart_page = cart_with_one_item
    cart_page.remove_product_from_cart(STEEL_WHITE)
    with allure.step("Verify the empty cart"):
        assert cart_page.empty_cart_title() == "Your cart is empty!"


@allure.epic("TestShop UI")
@allure.feature("Shopping cart")
@allure.title("Update one variant without changing another cart line")
@allure.description("Add Steel and Aluminium, increase only Aluminium, then remove Steel and verify the remaining line.")
def test_cart_lines_are_independent(driver):
    product_page = ProductPage(driver)
    product_page.open()
    product_page.add_to_cart()
    product_page.continue_shopping()
    product_page.wait_for_cart_quantity(1)

    product_page.open()
    product_page.select_aluminium()
    aluminium_price = product_page.get_price()
    product_page.add_to_cart()
    product_page.continue_shopping()
    product_page.wait_for_cart_quantity(2)

    cart_page = CartPage(driver)
    cart_page.open()
    with allure.step("Verify both variants have separate cart lines"):
        assert set(cart_page.get_product_names()) == {STEEL_WHITE, ALUMINIUM_WHITE}
        assert cart_page.get_product_quantity(STEEL_WHITE) == 1
        assert cart_page.get_product_quantity(ALUMINIUM_WHITE) == 1
        steel_price = cart_page.get_total_price(STEEL_WHITE)

    cart_page.increase_products_quantity(ALUMINIUM_WHITE)
    cart_page.wait_for_quantity(2, ALUMINIUM_WHITE)
    cart_page.wait_for_product_total(aluminium_price * 2, ALUMINIUM_WHITE)
    with allure.step("Verify that Steel was not changed"):
        assert cart_page.get_product_quantity(STEEL_WHITE) == 1
        assert cart_page.get_total_price(STEEL_WHITE) == steel_price

    cart_page.remove_product_from_cart(STEEL_WHITE)
    cart_page.wait_for_product_removed(STEEL_WHITE)
    with allure.step("Verify only Aluminium remains"):
        assert cart_page.get_product_names() == [ALUMINIUM_WHITE]
        assert cart_page.get_product_quantity(ALUMINIUM_WHITE) == 2
        assert cart_page.get_total_price(ALUMINIUM_WHITE) == aluminium_price * 2
