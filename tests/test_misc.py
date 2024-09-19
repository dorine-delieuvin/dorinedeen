import pytest
import re

from playwright.sync_api import Page, expect

"""
UI testing, using Playwright
test of the sections visible on all pages
or only on first connection
of the dorinedeen.wordpress.com website
"""


@pytest.fixture(scope="function", autouse=True)
def before_each_after_each(page: Page):
    # Go to the starting url before each test.
    page.goto("https://dorinedeen.wordpress.com")
    yield


pytestmark = pytest.mark.ui


@pytest.mark.cookies
def test_cookies_banner_visible(page: Page):
    expect(page.locator("id=eu_cookie_law_widget-3")).to_be_visible()


@pytest.mark.cookies
def test_cookies_accepted(page: Page):
    page.locator("input.accept").click()
    expect(page.locator("id=eu_cookie_law_widget-3")).not_to_be_visible()
