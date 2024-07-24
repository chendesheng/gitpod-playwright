import pytest
import os
from playwright.sync_api import BrowserContext

DOMAIN = "https://livechat6dash.testing.comm100dev.io"
EMAIL = "r@t.c"
PASSWORD = "Aa00000000"

SITE_ID = 10011
CAMPAIGN_ID = "daf7d2b9-85b3-42fa-b365-10fdc65039ba"

@pytest.fixture(scope="session")
def site_id():
    return SITE_ID

@pytest.fixture(scope="session")
def campaign_id():
    return CAMPAIGN_ID

import pytest
@pytest.fixture(scope="session")
def browser_context_args(request):
    return {"bypass_csp": True}

@pytest.fixture()
def control_panel_page(context: BrowserContext):
    page = context.new_page()
    page.goto(f'{DOMAIN}/login')
    return page

def get_token_from_cookie(context: BrowserContext, site_id: int):
    for cookie in context.cookies():
        if cookie['name'] == f"token_{site_id}":
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
    # create .auth if not exists
    if not os.path.exists(".auth"):
        os.makedirs(".auth")
    with open(".auth/token", 'wb') as file:
        file.write(token.encode())

@pytest.fixture()
def agent_console_page(context: BrowserContext, site_id: int):
    page = context.new_page()
    token = read_token_from_file()
    script = """((token, siteId, email) => {
        if (window.location.href.includes("/agentconsole/agentconsole.html")) {
            // when include partenrId in url, means it is jump from login page and don't need to place token in session storage
            if (!window.location.search.includes("partnerId") && token) window.sessionStorage.setItem(`auth_${siteId}`, JSON.stringify({token}));
            window.localStorage.setItem(`${email}_rememberStatus`, 'true');
            window.localStorage.setItem(`${email}_liveChatStatus`, 'online');
        }
    })""" + f"('{token}', {site_id}, '{EMAIL}')"
    # print(script)
    page.add_init_script(script)

    page.goto(f"{DOMAIN}/agentconsole/agentconsole.html?siteId={site_id}")
    # page.wait_for_url(re.compile("(.*\/agentconsole\/agentconsole\.html\?)|(.*\/login\?retUrl=)"))
    loaded_script = """() => {
        if (window.location.pathname.includes("/login")) {
            return 'login_page';
        } else if (document.querySelector("#dialog-title")?.textContent.trim() === "Force Login") {
            return 'force_login_dialog';
        } else if (document.querySelector("#app .MuiAvatar-root")){
            return 'agent_console';
        }
        return false;
    }"""
    res = page.wait_for_function(loaded_script).json_value()
    if res == "login_page":
        page.fill('input[name="email"]', EMAIL)
        page.fill('input[name="password"]', PASSWORD)
        page.click('button:has-text("Sign in")')
        page.wait_for_url("**/agentconsole/agentconsole.html?**")
        token = get_token_from_cookie(page.context, site_id)
        write_token_to_file(token)
        res = page.wait_for_function(loaded_script).json_value()
        if res == "force_login_dialog":
            page.click('button:has-text("OK")')
    elif res == "force_login_dialog":
        page.click('button:has-text("OK")')


    # try:
    #     page.wait_for_selector('.MuiDialogTitle-root:has-text("Choose Status")', timeout=5000)
    #     page.set_checked('input[type="checkbox"]', True)
    #     page.click('[role=menuitem]:has-text("Online")')
    #     page.click('button:has-text("OK")')
    # except TimeoutError:
    #     pass

    # page.click('//button[descendant::img[@class="MuiAvatar-img"]]')
    # page.click('[role=menuitem]:has-text("Log Out")')
    # page.wait_for_url("**/login?**")
    return page

@pytest.fixture()
def preview_visitor_page(context: BrowserContext, site_id: int, campaign_id: str):
    page = context.new_page()
    page.goto(f"{DOMAIN}/frontEnd/livechatpage/assets/livechat/previewpage/?siteId={site_id}&campaignId={campaign_id}")
    page.wait_for_selector('#comm100-iframe', state='attached')
    return page
