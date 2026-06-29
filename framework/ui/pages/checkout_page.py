from playwright.sync_api import Page, expect

from .base_page import BasePage


class CheckoutPage(BasePage):
    """Covers the three checkout steps: Your Information -> Overview -> Finish."""

    def __init__(self, page: Page, base_url: str):
        super().__init__(page, base_url)
        self.first_name = page.get_by_test_id("firstName")
        self.last_name = page.get_by_test_id("lastName")
        self.postal_code = page.get_by_test_id("postalCode")
        self.continue_button = page.get_by_test_id("continue")
        self.finish_button = page.get_by_test_id("finish")
        self.complete_header = page.get_by_test_id("complete-header")

    def fill_information(self, first: str, last: str, postal: str):
        self.first_name.fill(first)
        self.last_name.fill(last)
        self.postal_code.fill(postal)

    def continue_to_overview(self):
        self.continue_button.click()

    def finish(self):
        self.finish_button.click()

    def expect_order_complete(self, text: str):
        expect(self.complete_header).to_be_visible()
        expect(self.complete_header).to_have_text(text)
