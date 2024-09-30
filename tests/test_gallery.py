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
    # images have caption
    images = page.query_selector_all(".wp-block-image")
    i = 0
    while i < len(images):
        expect(page.locator(".wp-block-image").locator(f"nth={i}")).to_be_visible()
        expect(page.locator("figcaption").locator(f"nth={i}")).not_to_be_empty()
        i += 1

    # buttons have no link, only text


# GET IN TOUCH button
@pytest.mark.get_in_touch
def test_get_in_touch_gallery(page: Page):
    page.locator("a.wp-block-button__link", has_text="GET IN TOUCH").click()
    expect(page).to_have_url(re.compile(f".*/contact*"))
