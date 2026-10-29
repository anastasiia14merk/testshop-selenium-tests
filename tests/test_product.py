import allure

from data import ALUMINIUM_WHITE, DESK_NAME, STEEL_WHITE
from pages.cart_page import CartPage
from pages.desks_page import DesksPage
from pages.product_page import ProductPage


@allure.epic("TestShop UI")
@allure.feature("Product page")
@allure.title("Open the Customizable Desk product page")
@allure.description("Open the desk from its category and verify the product name.")
def test_open_customizable_desk(driver):
    desk_page = DesksPage(driver)
    desk_page.open()
    desk_page.open_customizable_desk()

    product_page = ProductPage(driver)
    with allure.step("Verify the product name"):
        assert product_page.get_product_name() == DESK_NAME


@allure.epic("TestShop UI")
@allure.feature("Product page")
@allure.title("Add the Aluminium variant to the cart")
@allure.description("Select Aluminium and verify its variant, quantity and price in the cart.")
def test_select_aluminium(driver):
    desk_page = DesksPage(driver)
    desk_page.open()
    desk_page.open_customizable_desk()

    product_page = ProductPage(driver)
    product_page.select_aluminium()
    with allure.step("Verify Aluminium is selected and read its price"):
        assert product_page.is_aluminium_selected()
        selected_price = product_page.get_price()
        assert selected_price > 0

    product_page.add_to_cart()
    product_page.continue_shopping()
    product_page.wait_for_cart_quantity(1)

    cart_page = CartPage(driver)
    cart_page.open()
    with allure.step("Verify the selected variant, quantity and price"):
        assert cart_page.get_product_name(ALUMINIUM_WHITE) == ALUMINIUM_WHITE
        assert cart_page.get_product_quantity(ALUMINIUM_WHITE) == 1
        assert cart_page.get_total_price(ALUMINIUM_WHITE) == selected_price


@allure.epic("TestShop UI")
@allure.feature("Product page")
@allure.title("Add two units selected on the product page")
@allure.description("Increase quantity from one to two and verify both units and their total in the cart after reloading.")
def test_increase_quantity(driver):
    product_page = ProductPage(driver)
    product_page.open()
    with allure.step("Verify the starting quantity and read the unit price"):
        assert product_page.get_quantity() == 1
        unit_price = product_page.get_price()
        assert unit_price > 0

    product_page.increase_quantity()
    product_page.wait_for_quantity(2)
    with allure.step("Verify the quantity on the product page"):
        assert product_page.get_quantity() == 2

    product_page.add_to_cart()
    product_page.continue_shopping()
    product_page.wait_for_cart_quantity(2)
    cart_page = CartPage(driver)
    cart_page.open()
    driver.refresh()
    cart_page.wait_for_page_ready()
    with allure.step("Verify that two units and their line total persist in the cart"):
        assert cart_page.get_product_quantity(STEEL_WHITE) == 2
        assert cart_page.get_total_price(STEEL_WHITE) == unit_price * 2
