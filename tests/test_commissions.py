import pytest
import re

from playwright.sync_api import Page, expect

"""
UI testing, using Playwright
test of the COMMISSIONS page of the dorinedeen.wordpress.com website
"""
pytestmark = pytest.mark.ui
pytestmark2 = pytest.mark.commissions

page_name = "commissions"


## Tests Setup/Cleanup
# Go to the starting url before each test.
@pytest.fixture(scope="function", autouse=True)
def before_each_after_each(page: Page, home_page_url):
    page.goto(home_page_url + f"/{page_name}")
    yield


## Tests
# Page header
@pytest.mark.commissions_header
def test_commissions_header_and_url(page: Page):
    expect(page).to_have_url(re.compile(f".*/{page_name}*"))
    expect(page.locator("h1.entry-title")).to_be_visible()


@pytest.mark.commissions_header
def test_commissions_header_content(page: Page):
    expect(page.locator("div.wp-block-cover")).to_be_visible()
    expect(
        page.locator(
            "div.wp-block-cover__inner-container > div.wp-block-buttons > div.wp-block-button > a.wp-block-button__link"
        )
    ).to_be_visible()
    expect(
        page.locator(
            "div.wp-block-cover__inner-container > div.wp-block-buttons > div.wp-block-button > a.wp-block-button__link"
        )
    ).to_have_attribute("href", re.compile(f"./contact/"))


@pytest.mark.commissions_header
def test_commissions_lets_talk_button(page: Page):
    page.locator(
        "div.wp-block-cover__inner-container > div.wp-block-buttons > div.wp-block-button > a.wp-block-button__link"
    ).click()
    expect(page).to_have_url(re.compile(f"./contact/"))


# Page body
@pytest.mark.commissions_body
def test_commissions_categories():
    pass


@pytest.mark.commissions_body
def test_to_consider_section():
    pass


# Customer reviews
def test_customer_reviews():
    pass


# GET IN TOUCH button
@pytest.mark.get_in_touch
def test_get_in_touch_commissions(page: Page):
    page.locator("a.wp-block-button__link", has_text="GET IN TOUCH").click()
    expect(page).to_have_url(re.compile(f".*/contact*"))
