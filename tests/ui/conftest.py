import base64
import re
from pathlib import Path

import pytest
from playwright.sync_api import Page, expect

from config.settings import settings
from framework.ui.pages.login_page import LoginPage
from framework.ui.pages.inventory_page import InventoryPage


def pytest_configure(config):
    """Make settings.browser the single env-overridable default (QA_BROWSER).

    pytest-playwright selects the engine from --browser. If it was not passed on
    the CLI, we inject the configured value so the browser is externalised
    config, not a value hardcoded in the CI command.
    """
    if not config.option.browser:
        config.option.browser = [settings.browser]


@pytest.fixture(scope="session", autouse=True)
def configure_playwright(playwright):
    """Session-wide Playwright setup.

    - Map get_by_test_id(...) to Swag Labs' data-test attribute (it defaults to
      data-testid), so page objects can use the expressive test-id API.
    - Apply the configured timeout to web-first assertions, so the externalised
      timeout actually governs UI waits instead of Playwright's 5s default.
    """
    playwright.selectors.set_test_id_attribute("data-test")
    expect.set_options(timeout=settings.timeout_ms)


@pytest.fixture(autouse=True)
def apply_default_timeout(page: Page):
    # Apply the configured timeout to all actions/navigations on this page.
    page.set_default_timeout(settings.timeout_ms)


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    # The `page` fixture (from pytest-playwright) creates a fresh, isolated
    # BrowserContext per test, so every test starts from a clean session.
    return LoginPage(page, settings.base_web_url).open()


@pytest.fixture
def inventory_page(login_page: LoginPage) -> InventoryPage:
    """A logged-in inventory page: per-test setup for tests that start after
    login. Each test owns this setup; no shared logged-in session is reused."""
    inventory = login_page.login(settings.standard_user, settings.password)
    inventory.expect_loaded()
    return inventory


# --- Reporting: link failure artifacts into the HTML report ----------------
# pytest-playwright writes screenshot/trace/video into --output during fixture
# teardown. We embed the screenshot and link the trace into the pytest-html row
# so an on-call engineer sees the evidence in the HTML report, without hunting
# through test-results/ by hand.


def _artifact_dir(item) -> Path | None:
    output = Path(item.config.getoption("--output") or "test-results")
    if not output.exists():
        return None
    # pytest-playwright derives the folder name from the test node id; match by
    # the slugified test name (e.g. "test_login_happy_path[chromium]").
    slug = re.sub(r"[^0-9A-Za-z]+", "-", item.name).strip("-")
    dirs = [d for d in output.iterdir() if d.is_dir() and slug in d.name]
    return max(dirs, key=lambda d: d.stat().st_mtime) if dirs else None


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        item._ui_failed = True

    # Artifacts exist only after teardown, so attach them on the teardown report.
    if report.when == "teardown" and getattr(item, "_ui_failed", False):
        html = item.config.pluginmanager.getplugin("html")
        artifact_dir = _artifact_dir(item)
        if html is None or artifact_dir is None:
            return
        extras = list(getattr(report, "extras", []))
        screenshot = artifact_dir / "test-failed-1.png"
        if screenshot.exists():
            encoded = base64.b64encode(screenshot.read_bytes()).decode()
            extras.append(html.extras.image(encoded, name="screenshot"))
        trace = artifact_dir / "trace.zip"
        if trace.exists():
            extras.append(html.extras.url(str(trace), name="trace.zip"))
        report.extras = extras
