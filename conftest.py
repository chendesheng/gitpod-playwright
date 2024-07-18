import pytest
from playwright.sync_api import BrowserContext

import pytest
@pytest.fixture(scope="session")
def browser_context_args(request):
    return {"bypass_csp": True}

@pytest.fixture()
def control_panel_page(context: BrowserContext):
    page = context.new_page()
    page.goto('https://livechat6dash.testing.comm100dev.io/login')
    return page