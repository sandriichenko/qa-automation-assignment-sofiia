from playwright.sync_api import Page, expect

from .base_page import BasePage
from .inventory_page import InventoryPage


class LoginPage(BasePage):
    URL_PATH = "/"

    def __init__(self, page: Page, base_url: str):
        super().__init__(page, base_url)
        # Intent-based selectors. Swag Labs exposes data-test attributes, which
        # are mapped to get_by_test_id via the configure_playwright fixture.
        self.username = page.get_by_test_id("username")
        self.password = page.get_by_test_id("password")
        self.login_button = page.get_by_test_id("login-button")
        self.error = page.get_by_test_id("error")

    def login(self, user: str, pwd: str) -> InventoryPage:
        self.username.fill(user)
        self.password.fill(pwd)
        self.login_button.click()
        return InventoryPage(self.page, self.base_url)

    def expect_error(self, text: str):
        # Web-first assertions: poll until the error is visible and contains the
        # exact wording the app shows. If the copy changes, this fails loudly.
        expect(self.error).to_be_visible()
        expect(self.error).to_contain_text(text)
