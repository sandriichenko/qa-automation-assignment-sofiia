# Design Rationale

## Language and framework choice

**Python + Playwright + pytest.** Python keeps the framework small and readable;
pytest's fixture model maps cleanly onto "each test owns its setup/teardown".

**Playwright over Selenium.** Playwright's auto-waiting and web-first assertions
(`expect(locator).to_...`) remove an entire class of flakiness without any
explicit wait code: every action and assertion polls until the condition holds
or the timeout expires. It also ships the artifacts I need for triage — trace
(timeline + DOM snapshots + network), screenshots, video — as configuration, not
hand-written `try/except`. Per-test `BrowserContext` gives isolation for free.

**When I would pick Selenium instead:** a hard requirement to support a browser
Playwright doesn't (older/edge engines), an existing investment in Selenium Grid
and team expertise, or integration with tooling that only speaks WebDriver.

## Anti-flakiness strategy

Concrete techniques used here:

- **No `sleep`, no implicit waits.** All waiting is condition-based via
  Playwright auto-wait and web-first assertions.
- **Intent-based selectors.** `get_by_test_id` mapped to Swag Labs' `data-test`
  attribute; no brittle XPath/CSS chains.
- **Strong isolation.** Fresh `BrowserContext` per test and a fresh API client
  per test — order-independent, parallel-safe.
- **Connection-level retries only** in the API client (transport `retries=2`),
  never status-code retries, so real failures are never masked.
- **Meaningful assertions** (cart name+price together, schema validation via
  pydantic) so tests fail for the right reasons.

**At 1000+ tests** I would add: a quarantine lane for known-flaky tests, a
flakiness-rate dashboard, retry-with-tracking (record every retry, never hide
it), sharding across CI runners, and periodic nightly stability runs.

## Parallelism and isolation

Isolation is structural: every test gets its own browser context (cookies /
localStorage / sessionStorage) and its own API client, so there is no shared
mutable state. I use one shared **user** (`standard_user`) because Swag Labs only
offers fixed accounts — this is safe because the cart lives in the session's
localStorage, which the per-test context isolates.

**What breaks first as parallelism goes up:** for a real backend it would be
shared server-side data; here that doesn't exist, so the next limits are the
external API's rate limiting and the CI runner's CPU/RAM under concurrent
browsers. That's why the default is a modest `-n 2`.

## API testing against a simulated backend

JSONPlaceholder simulates writes: `POST`/`PUT`/`DELETE` return success but never
persist. This shapes two deliberate decisions:

- **No GET-after-DELETE assertion.** Verifying that a deleted resource is no
  longer retrievable is the correct check for a real API. Here it would fail —
  `DELETE /posts/1` returns 200 but `GET /posts/1` still returns the post —
  because nothing is actually removed. So we assert response shape/status, not
  persistence. **Against a real backend I would add `GET-after-DELETE -> 404`.**
- **No create-then-teardown fixture.** A fixture that creates a resource in
  setup and deletes it in teardown is the right isolation pattern for a real,
  stateful API. Against this sandbox there is nothing to tear down (the
  "created" id 101 is not really retrievable), so adding that lifecycle here
  would be ceremony with no payoff. Tests instead use the seeded id 1 and a
  small payload factory (`tests/api/factories.py`). **On a real API the
  create/teardown fixture is what I would build.**

## Reporting and triage (a 3am failure)

The on-call engineer opens the failed GitHub Actions run, downloads the
`test-report` artifact, and opens `report.html` to see which test failed and
why. For UI failures they open the captured `trace.zip` in the Playwright trace
viewer (`playwright show-trace ...`): a full timeline with DOM snapshots,
network, and console at the exact moment of failure — plus the screenshot and
video. Root cause is reachable in minutes, without reproducing locally.

## What I would do next (another two days)

- **Visual regression** on key screens to catch CSS/layout breakage.
- **API contract tests** (schema-drift detection) wired to the provider.
- A **deploy smoke suite** — a tiny critical-path subset gated on every deploy.
- **Allure reporting** with historical trends to track flakiness over time.

## AI tool usage

I used Claude to scaffold the page-object structure and CI workflow and to
review this document. All test logic, selectors, and assertions were verified by
hand against the live targets.


