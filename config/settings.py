"""Single source of truth for runtime configuration.

Everything that a CI job or a developer might want to override lives here and is
read from environment variables (prefix ``QA_``) with sensible defaults. No URLs,
credentials or timeouts are hardcoded inside tests or page objects.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="QA_", extra="ignore")

    # --- Web target: Swag Labs ---------------------------------------------
    base_web_url: str = "https://www.saucedemo.com"
    standard_user: str = "standard_user"
    password: str = "secret_sauce"

    # --- API target: JSONPlaceholder ---------------------------------------
    base_api_url: str = "https://jsonplaceholder.typicode.com"

    # --- Runtime knobs ------------------------------------------------------
    # Browser engine for the UI suite (chromium | firefox | webkit). Applied via
    # pytest_configure in tests/ui/conftest.py when --browser is not passed on
    # the CLI, so this is the single env-overridable default (QA_BROWSER).
    browser: str = "chromium"

    # Default wait/assertion timeout in milliseconds. Applied to Playwright via
    # page.set_default_timeout + expect.set_options (tests/ui/conftest.py) and
    # to the API client timeout (converted to seconds, see timeout_s).
    timeout_ms: int = 10_000

    @property
    def timeout_s(self) -> float:
        return self.timeout_ms / 1000


settings = Settings()
