"""Shared settings; environment overrides also work in CI."""

import os

BASE_URL = os.getenv("TESTSHOP_BASE_URL", "http://testshop.qa-practice.com")
WAIT_TIMEOUT = float(os.getenv("TESTSHOP_WAIT_TIMEOUT", "10"))
if WAIT_TIMEOUT <= 0:
    raise ValueError("TESTSHOP_WAIT_TIMEOUT must be greater than zero")
