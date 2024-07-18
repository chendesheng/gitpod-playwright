import pytest
import re
from playwright.sync_api import Page, Browser, BrowserContext, expect, TimeoutError
from playwright.sync_api import sync_playwright

from visual_regression_tracker import Config, IgnoreArea
from visual_regression_tracker.playwright import PlaywrightVisualRegressionTracker, PageTrackOptions, \
    PageScreenshotOptions, Agent, ElementHandleScreenshotOptions, ElementHandleTrackOptions

def test_login_ui(browser: Browser, control_panel_page: Page):
  control_panel_page.wait_for_timeout(10*1000)

  vrt = PlaywrightVisualRegressionTracker(browser.browser_type, None)

  with vrt:
      vrt.trackPage(control_panel_page, 'Home page', PageTrackOptions(
          diffTollerancePercent=1.34,
          ignoreAreas=[
              IgnoreArea(
                  x=100,
                  y=200,
                  width=300,
                  height=400,
              )
          ],
          screenshotOptions=PageScreenshotOptions(
              full_page=True,
              omit_background=True,
          ),
          agent=Agent(
              os='OS',
              device='Device',
          )
      ))
