import pytest

pytestmark = pytest.mark.api


def test_create_post_echoes_payload(api_client, post_payload):
    # Scenario 3: 201 Created, response echoes payload and includes an id.
    payload = post_payload(title="qa", body="lead")
    response = api_client.create_post(payload)

    assert response.status_code == 201
    body = response.json()
    assert body["title"] == payload["title"]
    assert body["body"] == payload["body"]
    assert body["userId"] == payload["userId"]
    assert "id" in body  # server-generated id


def test_update_post(api_client, post_payload):
    # Scenario 4a: PUT returns 200 with the updated body.
    payload = post_payload(id=1, title="updated title", body="updated body")
    response = api_client.update_post(1, payload)

    assert response.status_code == 200
    # Assert the whole updated body, not just one field (acceptance: "200 with
    # the updated body").
    body = response.json()
    assert body["id"] == payload["id"]
    assert body["title"] == payload["title"]
    assert body["body"] == payload["body"]
    assert body["userId"] == payload["userId"]


def test_delete_post(api_client):
    # Scenario 4b: DELETE returns 200 or 204. Writes are simulated, so we assert
    # the response shape/status, not persistence (see DESIGN.md). On a real API
    # we would additionally assert GET-after-DELETE returns 404.
    response = api_client.delete_post(1)
    assert response.status_code in (200, 204)
