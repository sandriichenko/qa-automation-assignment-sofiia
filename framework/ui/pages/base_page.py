from playwright.sync_api import Page


class BasePage:
    """Common base for all page objects.

    Intentionally thin: it does NOT wrap clicks or invent ``wait_for_element``
    helpers. Playwright already auto-waits on every action and web-first
    assertion, so adding our own waiting layer would only duplicate (and likely
    weaken) behaviour the framework gives us for free.
    """

    URL_PATH = ""

    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url

    def open(self):
        self.page.goto(f"{self.base_url}{self.URL_PATH}")
        return self
