import pytest

pytestmark = pytest.mark.ui


def test_e2e_checkout(inventory_page):
    # Scenario 4: add a product and walk the full checkout flow to completion.
    inventory_page.add_to_cart("sauce-labs-backpack")

    checkout = inventory_page.go_to_cart().start_checkout()
    checkout.fill_information("Test", "User", "01001")
    checkout.continue_to_overview()
    checkout.finish()
    checkout.expect_order_complete("Thank you for your order!")
