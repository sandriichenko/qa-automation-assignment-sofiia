from collections.abc import Callable, Iterator

import pytest

from config.settings import settings
from framework.api.client import JsonPlaceholderClient


@pytest.fixture
def api_client() -> Iterator[JsonPlaceholderClient]:
    # Each test owns its own client and closes it in teardown -> no shared
    # mutable state between tests, parallel-safe by construction.
    client = JsonPlaceholderClient(settings.base_api_url, timeout=settings.timeout_s)
    yield client
    client.close()


@pytest.fixture
def post_payload() -> Callable[..., dict]:
    """Factory for /posts request bodies.

    Exposed via conftest (not a bare module import) so tests stay decoupled from
    import-path mechanics. Overrides let a test change only the field it asserts
    on while a single place owns the default shape.
    """

    def _make(**overrides: object) -> dict:
        payload: dict = {"title": "qa", "body": "lead", "userId": 1}
        payload.update(overrides)
        return payload

    return _make
