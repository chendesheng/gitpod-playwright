import pytest
from playwright.sync_api import sync_playwright

import pytest
@pytest.fixture(scope="session")
def browser_context_args(request):
    return {"bypass_csp": True}
