import allure
import pytest
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

from data import STEEL_WHITE
from pages.cart_page import CartPage
from pages.product_page import ProductPage


@pytest.fixture
@allure.title("Chrome browser")
def driver():
    browser = webdriver.Chrome()
    try:
        browser.maximize_window()
        yield browser
    finally:
        browser.quit()


@pytest.fixture
@allure.title("Cart containing one Steel, White desk")
def cart_with_one_item(driver):
    product_page = ProductPage(driver)
    product_page.open()
    product_page.add_to_cart()
    product_page.continue_shopping()
    product_page.wait_for_cart_quantity(1)

    cart_page = CartPage(driver)
    cart_page.open()
    assert cart_page.get_product_quantity(STEEL_WHITE) == 1
    return cart_page


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if not report.failed or report.when not in ("setup", "call"):
        return
    browser = item.funcargs.get("driver")
    if browser is None:
        return

    attachments = (
        ("Screenshot on failure", browser.get_screenshot_as_png, allure.attachment_type.PNG),
        ("Current page URL", lambda: browser.current_url, allure.attachment_type.TEXT),
        ("Page HTML on failure", lambda: browser.page_source, allure.attachment_type.HTML),
    )
    for name, read_value, attachment_type in attachments:
        try:
            allure.attach(read_value(), name=name, attachment_type=attachment_type)
        except WebDriverException:
            continue
