import pytest
import re

from playwright.sync_api import Page, expect


pytestmark = pytest.mark.ui
home_page_url = "https://dorinedeen.wordpress.com"

"""
UI testing, using Playwright

test of the sections visible on all pages
or only on first connection to the
dorinedeen.wordpress.com website
"""


## Tests Setup/Cleanup


@pytest.fixture(scope="function", autouse=True)
def before_each_after_each(page: Page):
    # Go to the starting url before each test.
    page.goto(home_page_url)
    yield


## Data sets for parametrization
page_urls = [
    "",
    "/gallery",
    "/comissions",
    "/contact",
]


## Tests


@pytest.mark.cookies
def test_cookie_banner_visible(page: Page):
    expect(page.locator("id=eu_cookie_law_widget-3")).to_be_visible()
    expect(page.locator("a.Cookie Policy")).to_be_visible


@pytest.mark.cookies
def test_cookies_accepted(page: Page):
    page.locator("input.accept").click()
    expect(page.locator("id=eu_cookie_law_widget-3")).not_to_be_visible()


@pytest.mark.site_header
def test_site_header_content_visible(page: Page):
    expect(page.locator("div.site-logo")).to_be_visible()
    expect(page.locator("p.site-title")).to_be_visible()
    expect(page.locator("p.site-description")).to_be_visible()
    expect(page.locator("id=menu-social")).to_be_visible()
    expect(page.locator("id=site-navigation")).to_be_visible()


@pytest.mark.site_header
@pytest.mark.parametrize("page_url", page_urls)
def test_site_header_visible_on_all_pages(page: Page, page_url):
    page.goto(home_page_url + page_url)
    expect(page.locator("id=masthead")).to_be_visible
