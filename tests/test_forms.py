import pytest
from framework.handlers.form import FormHandler


@pytest.mark.skip(reason="Target site does not have a suitable contact form for this test")
@pytest.mark.regression
def test_fill_and_submit_contact_form(actions):
    form_handler = FormHandler(actions)

    actions.ai_click("the 'Contact Us' link")

    form_data = {
        "full name": "Test User",
        "email address": "test@example.com",
        "subject": "Testing the form",
        "your message": "This is an automated test message."
    }

    form_handler.fill_form(form_data)
    form_handler.submit_form("the 'Send Message' button")

    confirmation = form_handler.get_confirmation_message()
    assert confirmation is not None
    assert "Your message has been sent" in confirmation