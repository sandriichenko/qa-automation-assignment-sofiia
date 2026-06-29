"""API scenarios 1 & 2.

The assignment defines 4 scenarios; we keep them as atomic tests (one reason to
fail each) and map them explicitly:
  - Scenario 1 (GET /posts)        -> test_get_posts_returns_array
  - Scenario 2 (GET /posts/{id})   -> test_get_post_valid_id (200)
                                       test_get_post_not_found (404)
Scenarios 3 & 4 live in test_posts_write.py.
"""

import pytest

from framework.api.schemas import Post

pytestmark = pytest.mark.api


def test_get_posts_returns_array(api_client):
    # Scenario 1: 200 OK, JSON array, known length, item schema validated.
    response = api_client.get_posts()
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    # Intentional exact-count assertion: JSONPlaceholder's /posts is a stable,
    # documented contract of 100 items. Asserting the exact length is a stronger
    # check than ">= 1"; if the count ever changes we want to know.
    assert len(data) == 100
    Post(**data[0])  # raises ValidationError if the item schema drifts


def test_get_post_valid_id(api_client):
    # Scenario 2a: 200 OK for a valid id.
    response = api_client.get_post(1)
    assert response.status_code == 200
    Post(**response.json())


def test_get_post_not_found(api_client):
    # Scenario 2b: 404 for a non-existent id.
    response = api_client.get_post(99999)
    assert response.status_code == 404
