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
def test_commissions_categories(page: Page):
    categories = page.query_selector_all(
        "div.wp-block-jetpack-layout-grid-column > h2.wp-block-heading"
    )
    i = 0
    while i < len(categories):
        # titles
        expect(
            page.locator(
                "div.wp-block-jetpack-layout-grid-column > h2.wp-block-heading"
            ).locator(f"nth={i}")
        ).not_to_be_empty()

        # descriptions
        expect(
            page.locator(
                "div.wp-block-jetpack-layout-grid-column > ul.wp-block-list"
            ).locator(f"nth={i}")
        ).not_to_be_empty()

        # prices
        expect(
            page.locator(
                "div.wp-block-jetpack-layout-grid-column > h2.wp-block-heading"
            )
            .locator("//following-sibling::*[1]")
            .locator(f"nth={i}")
        ).to_have_text(re.compile("[*£*]"))
        i += 1

    # images display
    images = page.query_selector_all("div.wp-block-jetpack-layout-grid-column img")
    i = 0
    while i < len(images):
        expect(
            page.locator("div.wp-block-jetpack-layout-grid-column img").locator(
                f"nth={i}"
            )
        ).to_be_visible()
        i += 1


@pytest.mark.commissions_body
def test_to_consider_section(page: Page):
    expect(
        page.locator(
            "div.entry-content > div.wp-block-group > div.wp-block-group__inner-container > div.wp-block-group > div.wp-block-group__inner-container"
        )
    ).not_to_be_empty()

    # check hyperlink
    expect(
        page.locator(
            "div.entry-content > div.wp-block-group > div.wp-block-group__inner-container > div.wp-block-group > div.wp-block-group__inner-container > p > a"
        )
    ).to_have_text("Contact me")
    expect(
        page.locator(
            "div.entry-content > div.wp-block-group > div.wp-block-group__inner-container > div.wp-block-group > div.wp-block-group__inner-container > p > a"
        )
    ).to_have_attribute("href", re.compile("./contact/*"))


# Customer reviews
def test_customer_reviews(page: Page):
    #
    expect(
        page.locator(".wp-block-jetpack-layout-grid-column > p > em > em")
    ).not_to_be_empty()
    expect(
        page.locator(".wp-block-jetpack-layout-grid-column > p > a")
    ).to_have_attribute("href", re.compile("https://*"))


# GET IN TOUCH button
@pytest.mark.get_in_touch
def test_get_in_touch_commissions(page: Page):
    page.locator("a.wp-block-button__link", has_text="GET IN TOUCH").click()
    expect(page).to_have_url(re.compile(f".*/contact*"))
