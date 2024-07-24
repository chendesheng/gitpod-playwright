from playwright.sync_api import expect, Page


def test_send_chat_message(preview_visitor_page: Page, agent_console_page: Page, campaign_id: str):
    chat_button_frame = preview_visitor_page.frame_locator(f'#comm100-button-{campaign_id} iframe')
    chat_button_frame.locator('[role=button]').click()
    preview_visitor_page.wait_for_selector('iframe#chat_window_container')
    chat_window_frame = preview_visitor_page.frame_locator('iframe#chat_window_container')
    chat_input = chat_window_frame.locator('.window__chatInputControl')
    chat_input.fill("How are you?")
    chat_input.press("Enter")
    agent_console_page.click('[role=menuitem][aria-label="Live Chat"]')
    message = agent_console_page.locator('//div[contains(@class, "ChatMessageBubble-module__container") and contains(normalize-space(.), "How are you?")]')
    expect(message).to_be_visible(timeout=10000)


def test_login_ui(control_panel_page: Page, assert_snapshot):
  control_panel_page.wait_for_load_state('networkidle')
  assert_snapshot(control_panel_page.screenshot())

