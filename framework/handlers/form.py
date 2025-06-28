from selenium.common.exceptions import NoSuchElementException


class FormHandler:
    def __init__(self, actions):
        self.actions = actions

    def fill_form(self, field_data: dict):
        for field_description, value in field_data.items():
            self.actions.ai_type(f"the form field for '{field_description}'", value)

    def submit_form(self, button_description="the submit button"):
        self.actions.ai_click(button_description)

    def get_confirmation_message(self):
        try:
            element = self.actions.ai_find_element("the form submission success message")
            return element.text
        except NoSuchElementException:
            return None