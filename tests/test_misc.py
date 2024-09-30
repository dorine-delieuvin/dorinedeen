import pytest
import re

from playwright.sync_api import Page, expect


"""
UI testing, using Playwright

test of the sections visible on all pages
or only on first connection to the
dorinedeen.wordpress.com website
"""
pytestmark = pytest.mark.ui


## Tests Setup/Cleanup
# Go to the starting url before each test.
@pytest.fixture(scope="function", autouse=True)
def before_each_after_each(page: Page, home_page_url):
    page.goto(home_page_url)
    yield


## Data sets for parametrization
# page_urls = [list of the page urls for the website]
page_urls = [
    "",  # Home page
    "/gallery",
    "/commissions",
    "/contact",
]

# menu_buttons = [(nth button of pages menu, "url of destination page")]
menu_buttons = [
    (0, "/"),  # Home page
    (1, "/gallery"),
    (2, "/commissions"),
    (3, "/contact"),
]


## Tests
# Cookie banner
@pytest.mark.cookies
def test_cookie_banner_visible(page: Page):
    expect(page.locator("id=eu_cookie_law_widget-3")).to_be_visible()
    expect(page.locator("a.Cookie Policy")).to_be_visible


@pytest.mark.cookies
def test_cookies_accepted(page: Page):
    page.locator("input.accept").click()
    expect(page.locator("id=eu_cookie_law_widget-3")).not_to_be_visible()


# Site header
@pytest.mark.site_header
def test_site_header_content_visible(page: Page):
    expect(page.locator("div.site-logo")).to_be_visible()
    expect(page.locator("p.site-title")).to_be_visible()
    expect(page.locator("p.site-description")).to_be_visible()
    expect(page.locator("id=menu-social")).to_be_visible()
    expect(page.locator("id=site-navigation")).to_be_visible()


@pytest.mark.site_header
@pytest.mark.parametrize("page_url", page_urls)
def test_site_header_visible_on_all_pages(page: Page, home_page_url, page_url):
    page.goto(home_page_url + page_url)
    expect(page.locator("id=masthead")).to_be_visible


@pytest.mark.site_header
@pytest.mark.parametrize("button", menu_buttons)
def test_menu_button_links(page: Page, button):
    page.locator("li.menu-item").locator(f"nth={button[0]}").click()
    expect(page).to_have_url(re.compile(f".*{button[1]}"))


# Site footer
@pytest.mark.site_footer
def test_site_footer_content_visible(page: Page):
    expect(page.locator("id=menu-social-1")).to_be_visible()
    expect(page.locator("div.site-info")).to_be_visible()

    # checking whether the hyperlinks in the copyrights section contain a link redirecting to the respective websites
    expect(page.locator("div.site-info > a.site-name")).to_have_attribute(
        "href", re.compile("https://dorinedeen*")
    )
    expect(page.locator("div.site-info > a").locator("nth=1")).to_have_attribute(
        "href", re.compile("https://wordpress.com*")
    )


@pytest.mark.site_footer
@pytest.mark.parametrize("page_url", page_urls)
def test_site_footer_visible_on_all_pages(page: Page, home_page_url, page_url):
    page.goto(home_page_url + page_url)
    expect(page.locator("id=colophon")).to_be_visible
