import pytest

pytestmark = pytest.mark.ui


def test_add_two_products_to_cart(inventory_page):
    # Scenario 3: add two distinct products and verify badge + cart contents.
    inventory_page.add_to_cart("sauce-labs-backpack")
    inventory_page.add_to_cart("sauce-labs-bike-light")
    inventory_page.expect_badge_count(2)

    cart = inventory_page.go_to_cart()
    cart.expect_item_count(2)
    cart.expect_item("Sauce Labs Backpack", "$29.99")
    cart.expect_item("Sauce Labs Bike Light", "$9.99")
