import pytest
import re

from playwright.sync_api import Page, expect

"""
UI testing, using Playwright
test of the CONTACT page of the dorinedeen.wordpress.com website
"""
pytestmark = pytest.mark.ui
pytestmark2 = pytest.mark.contact

page_name = "contact"

## Data sets for parametrization
# required_fields = ["Field CSS locator"]
required_fields = [
    "label.grunion-field-label.name",
    "label.grunion-field-label.email",
    "label.grunion-field-label.textarea",
]


## Tests Setup/Cleanup
# Go to the starting url before each test.
@pytest.fixture(scope="function", autouse=True)
def before_each_after_each(page: Page, home_page_url):
    page.goto(home_page_url + f"/{page_name}")
    yield


## Tests
# Page header and url
def test_contact_title_and_url(page: Page):
    expect(page).to_have_url(re.compile(f".*/{page_name}*"))
    expect(page.locator("h1.entry-title")).to_be_visible()


# Form
@pytest.mark.contact_form
def test_form_display(page: Page):
    expect(page.locator("id=contact-form-7")).to_be_visible()
    expect(page.locator("button.wp-block-button__link")).to_be_visible()


@pytest.mark.contact_form
@pytest.mark.parametrize("field", required_fields)
def test_form_required_fields(page: Page, field):
    expect(page.locator(field)).to_be_visible()
    expect(page.locator(field)).to_have_text(re.compile(".*required.*"))


# Contact card
