# TestShop Selenium UI Tests

UI test automation for [TestShop](http://testshop.qa-practice.com/) using Python,
Selenium WebDriver, pytest, Allure and the Page Object Model (POM).
The educational suite contains **ten independent UI scenarios**.

## Test coverage

| Page | Scenarios |
| --- | --- |
| Shopping cart | Add a desk; increase quantity and check the line total; remove the last unit; keep Steel and Aluminium cart lines independent when updating/removing them |
| Product page | Navigate from the category; select Aluminium and verify its variant/price in the cart; select two units and verify their quantity/total persist in the cart after reload |
| Desks category | Check the breadcrumb; validate positive numeric card prices and compare the default desk price across catalog/product/cart; apply list layout and preserve product names, prices and order |

## Project structure

```text
pages/
    base_page.py       # Shared navigation, application readiness and waits
    cart_page.py       # Operations scoped to a named product/variant row
    product_page.py    # Variant, quantity and options-dialog interactions
    desks_page.py      # Category cards and actual list-layout state
tests/                 # Cart, product and category scenarios
config.py              # Base URL and timeout, with environment overrides
data.py                # Shared catalog and variant names
conftest.py            # Chrome options, fixtures and failure attachments
pytest.ini             # Test discovery and Allure output
requirements.txt       # Pinned Python dependencies
.github/workflows/
    ui-tests.yml       # GitHub Actions headless Chrome run and result artifacts
```

Page objects contain browser actions; scenario-specific assertions stay in tests.
Every test has a fresh Chrome session. Browser cleanup also runs if setup fails
after Chrome has been created.

## Synchronization

TestShop uses Odoo and initializes application event handlers after the HTML has
loaded. `BasePage.wait_for_page_ready()` first waits for the application's
`root.widget` module to load, then uses a short `execute_async_script` call to wait
for its startup promise. No temporary flags are added to the browser window. A visible/enabled button alone is not treated
as proof that the application is ready. If application startup fails, the wait fails
rather than silently clicking early.

Variant changes wait for the product variant ID to update. The options dialog is
located by its role in the page (`oe_advanced_configurator_modal`), not a generated
`modal_5` ID. `continue_shopping()` only closes that dialog; callers separately use
`wait_for_cart_quantity(expected_quantity)` to wait for the completed cart update.

Cart methods take a product's full variant name and re-find that same row during
updates. Price calculations use `Decimal` with TestShop's en_US number format.

## Prerequisites and setup

- Python 3.14 (local environment: Python 3.14.2).
- Google Chrome.
- Internet access to TestShop and, on first use, Selenium Manager's driver download.
- Allure CLI and Java are needed only to generate/view an Allure report.
  See the [official installation instructions](https://allurereport.org/docs/install/).

Run from the repository root:

```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows, activate with `venv\Scripts\activate` instead.

## Run tests

```bash
python -m pytest -v
python -m pytest --headless -v
python -m pytest --headless --window-size=1440,1000 -v
```

The default is a visible, maximized Chrome window. Headless mode defaults to
1920 by 1080 pixels. Set `CHROME_BINARY` if Chrome is installed at a custom path.

Run one file or scenario:

```bash
python -m pytest tests/test_product.py -v
python -m pytest tests/test_product.py::test_select_aluminium -v
```

`config.py` supplies the shared base URL and wait timeout. Environment overrides:

```bash
TESTSHOP_WAIT_TIMEOUT=20 python -m pytest --headless -v
TESTSHOP_BASE_URL=http://testshop.qa-practice.com python -m pytest -v
```

The base URL must point to a compatible TestShop/Odoo environment with this catalog.
A longer timeout does not replace waiting for the correct application state.

Allure results are written to `allure-results/`. Each invocation clears that target
directory. To preserve another run, supply `--alluredir=another-results-directory`.
Do not run simultaneous processes against the same results directory.

## Allure report

```bash
allure serve allure-results
```

Or generate a saved report:

```bash
allure generate allure-results --clean -o allure-report
allure open allure-report
```

For an Allure CLI supporting portable single-file reports:

```bash
allure generate allure-results --clean --single-file -o allure-report
```

On a setup/test failure, a screenshot, current URL and page HTML are attached when
available. Each attachment is collected independently, so a browser error does not
hide the test failure or prevent the remaining attachments.

## GitHub Actions

The workflow runs the suite in headless Chrome on pushes and pull requests, and can
also be started manually. It saves Allure results (including failure attachments)
and a JUnit XML summary as `ui-test-results` artifacts for seven days.
A local run does not confirm that a workflow has run on GitHub; check its Actions
status after publishing the changes.

## Scope and assumptions

- The suite uses Customizable Desk, its Steel/Aluminium variants and White color.
- Variant names identify distinct cart rows; duplicate names would need a different
  stable row key. `get_product_names()` waits for a nonempty cart; the empty-cart
  scenario uses `empty_cart_title()` instead.
- Category checks cover the currently loaded page, not pagination.
- Price assertions compare pre-tax product line totals, excluding delivery.
- All currently loaded desks must have a name and a positive numeric price.
- The public training site's availability/catalog are external dependencies.
- No account credentials are required, and no checkout/payment is submitted.

Generated results/reports, virtual environments, IDE settings and Python caches are
excluded from version control.
