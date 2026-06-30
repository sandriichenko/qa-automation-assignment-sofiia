import httpx


class JsonPlaceholderClient:
    """Thin wrapper over httpx.

    One place to change the base URL, default headers, timeout and the
    connection-level retry policy. Tests call intent-named methods and never
    construct URLs themselves.
    """

    def __init__(self, base_url: str, timeout: float = 10.0) -> None:
        # Retries here are transport-level (DNS/connect/read glitches), NOT
        # status-code retries -- we never mask a real 404/500 from the API.
        transport = httpx.HTTPTransport(retries=2)
        self._client = httpx.Client(
            base_url=base_url,
            timeout=timeout,
            headers={"Content-Type": "application/json; charset=UTF-8"},
            transport=transport,
        )

    def get_posts(self) -> httpx.Response:
        return self._client.get("/posts")

    def get_post(self, post_id: int) -> httpx.Response:
        return self._client.get(f"/posts/{post_id}")

    def create_post(self, payload: dict) -> httpx.Response:
        return self._client.post("/posts", json=payload)

    def update_post(self, post_id: int, payload: dict) -> httpx.Response:
        return self._client.put(f"/posts/{post_id}", json=payload)

    def delete_post(self, post_id: int) -> httpx.Response:
        return self._client.delete(f"/posts/{post_id}")

    def close(self) -> None:
        self._client.close()
