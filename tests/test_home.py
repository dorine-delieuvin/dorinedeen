import pytest
import re

from playwright.sync_api import Page, expect

"""
UI testing, using Playwright
test of the HOME page of the dorinedeen.wordpress.com website
"""
pytestmark = pytest.mark.ui
pytestmark2 = pytest.mark.home


## Tests Setup/Cleanup
# Go to the starting url before each test.
@pytest.fixture(scope="function", autouse=True)
def before_each_after_each(page: Page, home_page_url):
    page.goto(home_page_url)
    yield


## Tests
# Links tree
@pytest.mark.get_in_touch
def test_links_tree(page: Page):
    # checking the links tree and background image are visible
    expect(page.locator("div.wp-block-cover")).to_be_visible()
    expect(page.locator("div.wp-block-cover__inner-container")).to_be_visible()

    # checking all buttons on the link tree have the role "link" and a link attached in "href"
    # NOTE: one button is the "GET IN TOUCH" button at the bottom of the page
    buttons = page.query_selector_all("a.wp-block-button__link")
    i = 0
    while i < len(buttons):
        expect(
            page.locator("a.wp-block-button__link").locator(f"nth={i}")
        ).to_have_role("link")
        expect(
            page.locator("a.wp-block-button__link").locator(f"nth={i}")
        ).to_have_attribute("href", re.compile("https://*"))
        i += 1


# Home page body content
def test_home_page_body(page: Page):
    # check image and header are visible
    expect(page.locator("img.wp-image-46")).to_be_visible()
    expect(page.locator("h2.wp-block-heading")).to_be_visible()

    # check whether all paragraphs are visible
    body = page.query_selector_all("p.has-text-align-justify")
    i = 0
    while i < len(body):
        expect(
            page.locator("p.has-text-align-justify").locator(f"nth={i}")
        ).to_be_visible()
        i += 1


# GET IN TOUCH button
# tested whether link present with "test_links_tree"
@pytest.mark.get_in_touch
def test_get_in_touch_home(page: Page):
    page.locator("a.wp-block-button__link", has_text="GET IN TOUCH").click()
    expect(page).to_have_url(re.compile(f".*/contact*"))
