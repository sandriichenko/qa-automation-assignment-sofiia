# QA Automation Assignment

UI tests against [Swag Labs](https://www.saucedemo.com/) and API tests against
[JSONPlaceholder](https://jsonplaceholder.typicode.com/), built with **Python +
Playwright + pytest**.

See [DESIGN.md](DESIGN.md) for the rationale behind every choice.

## Prerequisites

- Python 3.11+
- macOS / Linux / Windows

## Setup (under 5 minutes)

```bash
git clone https://github.com/sandriichenko/qa-automation-assignment-sofiia.git
cd qa-automation-assignment-sofiia

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -e .
playwright install chromium        # add --with-deps on Linux to pull OS libs
```

## Run locally

```bash
pytest                  # everything (UI + API)
pytest tests/api        # API only
pytest tests/ui         # UI only
pytest -m ui            # by marker (ui / api)
pytest --headed         # watch the browser
```

## Run in parallel

```bash
pytest -n 2             # two pytest-xdist workers
pytest -n auto          # one worker per CPU core
```

Tests are parallel-safe: each UI test gets its own isolated `BrowserContext`
and each API test its own client, so there is no shared mutable state to
collide on.

## Reports & failure artifacts

Every run produces a self-contained HTML report; failures also capture a
screenshot, a video, and a Playwright trace.

```bash
pytest                              # writes report.html + test-results/
open report.html                    # the HTML report

# Inspect a failure trace interactively:
playwright show-trace test-results/<test-folder>/trace.zip
```

In CI these are uploaded as the **`test-report`** artifact on every run
(including failures) and are downloadable from the GitHub Actions run page.

## Configuration

All config lives in [config/settings.py](config/settings.py) and is overridable
via `QA_`-prefixed environment variables or a `.env` file (see
[.env.example](.env.example)). No URLs, credentials, or timeouts are hardcoded
in tests.

Common knobs:

```bash
QA_BROWSER=firefox pytest tests/ui     # browser: chromium | firefox | webkit
QA_TIMEOUT_MS=15000 pytest             # Playwright + API client timeout
```

The browser can also be set per-run with pytest-playwright's `--browser` flag,
which takes precedence over `QA_BROWSER`.

## CI

GitHub Actions workflow: [.github/workflows/tests.yml](.github/workflows/tests.yml).
Runs on every push and pull request to `main`.

Latest runs (all green on `main`):
https://github.com/sandriichenko/qa-automation-assignment-sofiia/actions/workflows/tests.yml?query=branch%3Amain
