import pytest
import re
from playwright.sync_api import Page, Browser, BrowserContext, expect, TimeoutError
import pytest_playwright_visual

def test_login_ui(browser: Browser, control_panel_page: Page, assert_snapshot):
  control_panel_page.wait_for_timeout(2*1000)
  assert_snapshot(control_panel_page.screenshot())

