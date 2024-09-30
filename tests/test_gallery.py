import pytest
import re

from playwright.sync_api import Page, expect

"""
UI testing, using Playwright
test of the GALLERY page of the dorinedeen.wordpress.com website
"""
pytestmark = pytest.mark.ui
pytestmark2 = pytest.mark.gallery

page_name = "gallery"


## Tests Setup/Cleanup
# Go to the starting url before each test.
@pytest.fixture(scope="function", autouse=True)
def before_each_after_each(page: Page, home_page_url):
    page.goto(home_page_url + f"/{page_name}")
    yield


## Tests
# Gallery header and url
def test_gallery_header_and_url(page: Page):
    expect(page).to_have_url(re.compile(f".*/{page_name}*"))
    expect(page.locator("h1.entry-title")).to_be_visible()


# Gallery content
def test_gallery_content(page: Page):
    # images display
    images = page.query_selector_all("img")
    i = 1  # not chcking the logo in the site header
    while i < len(images):
        expect(page.locator("img").locator(f"nth={i}")).to_be_visible
        i += 1
    # images have caption
    # buttons have no link, only text


# GET IN TOUCH button
@pytest.mark.get_in_touch
def test_get_in_touch_gallery(page: Page):
    page.locator("a.wp-block-button__link", has_text="GET IN TOUCH").click()
    expect(page).to_have_url(re.compile(f".*/contact*"))
