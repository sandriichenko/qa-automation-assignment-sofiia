import pytest

from config.settings import settings

pytestmark = pytest.mark.ui


def test_login_happy_path(inventory_page):
    # Scenario 1: login lands on the inventory page with items visible.
    # The login + landing assertion live in the inventory_page fixture, so the
    # test body only needs to confirm the post-condition.
    inventory_page.expect_loaded()


def test_login_invalid_credentials(login_page):
    # Scenario 2: wrong password shows the exact error the app renders.
    login_page.login(settings.standard_user, "wrong_password")
    login_page.expect_error(
        "Username and password do not match any user in this service"
    )
