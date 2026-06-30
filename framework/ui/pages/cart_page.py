from typing import TYPE_CHECKING

from playwright.sync_api import Page, expect

from .base_page import BasePage

if TYPE_CHECKING:
    from .checkout_page import CheckoutPage


class CartPage(BasePage):
    URL_PATH = "/cart.html"

    def __init__(self, page: Page, base_url: str) -> None:
        super().__init__(page, base_url)
        self.items = page.locator(".cart_item")
        self.checkout_button = page.get_by_test_id("checkout")

    def expect_item_count(self, count: int) -> None:
        expect(self.items).to_have_count(count)

    def expect_item(self, name: str, price: str) -> None:
        # Find the row that contains this product name, then assert its price.
        # This couples name and price together instead of checking them globally.
        row = self.items.filter(has_text=name)
        expect(row).to_be_visible()
        expect(row.get_by_test_id("inventory-item-price")).to_have_text(price)

    def start_checkout(self) -> "CheckoutPage":
        self.checkout_button.click()
        from .checkout_page import CheckoutPage

        return CheckoutPage(self.page, self.base_url)
