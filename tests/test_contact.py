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

# data to input = [("Name", "Email", "Message")]
field_inputs = [
    ("", "tester@email.com", "This is a test."),  # missing Name
    ("Tester", "", "This is a test."),  # missing email
    ("Tester", "tester@email.com", ""),  # missing message
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


@pytest.mark.contact_form
def test_form_submission_correct_input(page: Page):
    page.locator("id=g7-name").fill(f"Tester")
    page.locator("id=g7-email").fill("tester@email.com")
    page.locator("id=contact-form-comment-g7-message").fill("This is a test.")
    page.locator("button.wp-block-button__link").click()

    expect(page.locator("id=contact-form-success-header")).to_be_visible()


@pytest.mark.contact_form
@pytest.mark.parametrize("input", field_inputs)
def test_form_submission_incorrect_input(page: Page, input):
    page.locator("id=g7-name").fill(input[0])
    page.locator("id=g7-email").fill(input[1])
    page.locator("id=contact-form-comment-g7-message").fill(input[2])
    page.locator("button.wp-block-button__link").click()

    # success message not visible
    expect(page.locator("id=contact-form-success-header")).not_to_be_visible()

    # warning message display for missing fields
    if input[0] == "":
        expect(page.locator("id=g7-name-error")).to_be_visible()
    if input[1] == "":
        expect(page.locator("id=g7-email-error")).to_be_visible()
    if input[2] == "":
        expect(page.locator("id=g7-message-error")).to_be_visible()


# Contact card
def test_contact_card_display(page: Page):
    # logo and text should display
    expect(page.locator("img.wp-image-46")).to_be_visible()
    expect(page.locator("id=dorine-deen")).to_have_text("Dorine Deen")

    address = page.query_selector_all(".wp-block-column > p")
    i = 0
    while i < len(address):
        expect(
            page.locator(".wp-block-column > p").locator(f"nth={i}")
        ).not_to_be_empty()
        i += 1

    # social media buttons should display
    expect(page.locator("ul.wp-block-social-links")).to_be_visible()

    # buttons linked to hyperlinks
    social_links = page.query_selector_all(
        "ul.wp-block-social-links > li.wp-social-link"
    )
    i = 0
    while i < len(social_links):
        expect(
            page.locator("ul.wp-block-social-links > li.wp-social-link > a").locator(
                f"nth={i}"
            )
        ).to_have_attribute("href", re.compile("https://*"))
        i += 1
