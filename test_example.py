import pytest
import re
from playwright.sync_api import Page, BrowserContext, expect, TimeoutError
from playwright.sync_api import sync_playwright

SITE_ID = 10011
EMAIL = "r@t.c"
PASSWORD = "Aa00000000"

def get_token_from_cookie(context: BrowserContext):
    for cookie in context.cookies():
        if cookie['name'] == f"token_{SITE_ID}":
            return cookie['value']
    return None

def read_token_from_file():
    try:
        with open(".auth/token", 'rb') as file:
            return file.read().decode()
    except FileNotFoundError: 
        return ''
    except Exception as e:
        print(f'read token from file error: {e}')
        return ''

def write_token_to_file(token: str):
    with open(".auth/token", 'wb') as file:
        file.write(token.encode())

@pytest.fixture()
def agent_console_page(page: Page):

    token = read_token_from_file()
    script = """((token, siteId, email) => {
        if (window.location.href.includes("/agentconsole/agentconsole.html")) {
            if (token) window.sessionStorage.setItem(`auth_${siteId}`, JSON.stringify({token}));
            window.localStorage.setItem(`${email}_rememberStatus`, 'true');
            window.localStorage.setItem(`${email}_liveChatStatus`, 'online');
        }
    })""" + f"('{token}', {SITE_ID}, '{EMAIL}')"
    print(script)
    page.context.add_init_script(script)

    page.goto(f"https://livechat6dash.testing.comm100dev.io/agentconsole/agentconsole.html?siteId={SITE_ID}")
    # page.wait_for_url(re.compile("(.*\/agentconsole\/agentconsole\.html\?)|(.*\/login\?retUrl=)"))
    try:
        page.wait_for_url("**/login?**", timeout=5000)
        page.fill('input[name="email"]', EMAIL)
        page.fill('input[name="password"]', PASSWORD)
        page.click('button:has-text("Sign in")')
        page.wait_for_url("**/agentconsole/agentconsole.html?**")
        token = get_token_from_cookie(page.context)
        write_token_to_file(token)
    except TimeoutError:
        pass

    # try:
    #     page.wait_for_selector('.MuiDialogTitle-root:has-text("Choose Status")', timeout=5000)
    #     page.set_checked('input[type="checkbox"]', True)
    #     page.click('[role=menuitem]:has-text("Online")')
    #     page.click('button:has-text("OK")')
    # except TimeoutError:
    #     pass

    try:
        page.wait_for_selector('.MuiDialogTitle-root:has-text("Force Login")', timeout=5000)
        page.click('button:has-text("OK")')
    except TimeoutError:
        pass

    yield
    # page.click('//button[descendant::img[@class="MuiAvatar-img"]]')
    # page.click('[role=menuitem]:has-text("Log Out")')
    # page.wait_for_url("**/login?**")
    page.close()
    print("\nTeardown after all tests")

def test_has_title(agent_console_page, page: Page):
    expect(page).to_have_title(re.compile("Agent r t"), timeout=10000)
