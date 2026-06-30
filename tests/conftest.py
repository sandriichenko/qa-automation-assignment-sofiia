"""Shared pytest configuration for all tests (UI + API).

Holds only config hooks, no fixtures, so it does not leak anything into the
framework package -- fixtures still live in tests/ui and tests/api conftests.
"""

import os
from datetime import datetime

import pytest


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config: pytest.Config) -> None:
    """Write the HTML report under reports/.

    Locally the filename carries the run date/time (reports/report_<timestamp>.html)
    to keep a history of runs. In CI each run is already a separate artifact, so
    we use a stable reports/report.html that is easy to find and link.

    The path is set here (not in addopts) so it can vary per run; tryfirst makes
    this run before pytest-html reads the path. A single timestamp is shared
    across xdist workers via an env var, so a parallel run still yields one file.
    """
    reports_dir = config.rootpath / "reports"
    reports_dir.mkdir(exist_ok=True)
    if os.environ.get("CI"):
        filename = "report.html"
    else:
        stamp = os.environ.setdefault(
            "QA_REPORT_STAMP", datetime.now().strftime("%Y%m%d_%H%M%S")
        )
        filename = f"report_{stamp}.html"
    config.option.htmlpath = str(reports_dir / filename)
    config.option.self_contained_html = True
