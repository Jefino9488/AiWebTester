from selenium.common.exceptions import NoSuchElementException


class LoginHandler:
    def __init__(self, actions, config):
        self.actions = actions
        self.config = config

    def login(self, username, password):
        login_url = self.config['target_site']['login_url']
        self.actions.go_to(login_url)

        self.actions.ai_type("the username input field", username)
        self.actions.ai_type("the password input field", password)
        self.actions.ai_click("the login button")

    def get_logout_link_text(self):
        try:
            element = self.actions.ai_find_element("the logout link")
            return element.text
        except NoSuchElementException:
            return None

    def get_error_message(self):
        try:
            element = self.actions.ai_find_element("the login error message box")
            return element.text
        except NoSuchElementException:
            return None