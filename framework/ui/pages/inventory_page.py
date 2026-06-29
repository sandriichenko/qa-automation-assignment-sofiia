from playwright.sync_api import Page, expect

from .base_page import BasePage


class InventoryPage(BasePage):
    URL_PATH = "/inventory.html"

    def __init__(self, page: Page, base_url: str):
        super().__init__(page, base_url)
        self.items = page.locator(".inventory_item")
        self.cart_badge = page.get_by_test_id("shopping-cart-badge")
        self.cart_link = page.get_by_test_id("shopping-cart-link")

    def expect_loaded(self):
        expect(self.page).to_have_url(f"{self.base_url}{self.URL_PATH}")
        expect(self.items.first).to_be_visible()

    def add_to_cart(self, product_slug: str):
        # e.g. product_slug="sauce-labs-backpack" ->
        # data-test="add-to-cart-sauce-labs-backpack"
        self.page.get_by_test_id(f"add-to-cart-{product_slug}").click()

    def expect_badge_count(self, count: int):
        expect(self.cart_badge).to_have_text(str(count))

    def go_to_cart(self):
        self.cart_link.click()
        # Imported lazily to avoid a circular import between page objects.
        from .cart_page import CartPage

        return CartPage(self.page, self.base_url)
