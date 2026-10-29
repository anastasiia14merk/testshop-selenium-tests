import allure

from data import DESK_NAME, STEEL_WHITE
from pages.cart_page import CartPage
from pages.desks_page import DesksPage
from pages.product_page import ProductPage


@allure.epic('TestShop UI')
@allure.feature('Desks category')
@allure.title('Verify the Desks category name')
@allure.description('Open the Desks category and verify its name in the breadcrumb.')
def test_desk_category_title(driver):
    desk_page = DesksPage(driver)
    desk_page.open()

    with allure.step('Verify the category name'):
        assert desk_page.get_category_name() == 'Desks'


@allure.epic('TestShop UI')
@allure.feature('Desks category')
@allure.title('Verify catalog prices and consistency with the product and cart')
@allure.description(
    'Check names and positive numeric prices on every loaded card, then compare '
    'the default desk price between the category, product page and cart.'
)
def test_products_have_names_and_prices(driver):
    desk_page = DesksPage(driver)
    desk_page.open()
    products = desk_page.get_products()

    with allure.step('Verify names and positive numeric prices'):
        assert products, 'The category contains no products'
        for product in products:
            assert product['name'], 'A product name is missing'
            assert product['price'] > 0, (
                f"Invalid price for {product['name']}: {product['price']}"
            )
        desks = [product for product in products if product['name'] == DESK_NAME]
        assert len(desks) == 1, 'The expected desk card is missing or duplicated'
        catalog_price = desks[0]['price']

    desk_page.open_customizable_desk()
    product_page = ProductPage(driver)
    with allure.step('Compare the product-page price with the catalog'):
        assert product_page.get_product_name() == DESK_NAME
        assert product_page.get_price() == catalog_price

    product_page.add_to_cart()
    product_page.continue_shopping()
    product_page.wait_for_cart_quantity(1)
    cart_page = CartPage(driver)
    cart_page.open()
    with allure.step('Compare the price of one desk in the cart with the catalog'):
        assert cart_page.get_product_quantity(STEEL_WHITE) == 1
        assert cart_page.get_total_price(STEEL_WHITE) == catalog_price


@allure.epic('TestShop UI')
@allure.feature('Desks category')
@allure.title('Apply list layout and preserve the products')
@allure.description(
    'Verify that the category actually changes from grid to list layout and '
    'preserves product names, numeric prices and order.'
)
def test_switch_to_list_view(driver):
    desk_page = DesksPage(driver)
    desk_page.open()
    products_before = desk_page.get_products()

    with allure.step('Verify the initial grid layout and loaded products'):
        assert products_before, 'The category contains no products'
        assert not desk_page.is_list_view(), 'The category already uses list layout'

    desk_page.switch_to_list_view()
    with allure.step('Verify the applied list layout'):
        assert desk_page.is_list_view(), 'The product container still uses grid layout'

    products_after = desk_page.get_products()
    with allure.step('Verify that products are preserved in list view'):
        assert products_after == products_before, (
            'Product names, prices or order changed after switching the view'
        )
