from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class Actions:
    def __init__(self, driver, ai_finder, default_wait=10):
        self.driver = driver
        self.ai_finder = ai_finder
        self.default_wait = default_wait

    def _find_element(self, locator):
        return WebDriverWait(self.driver, self.default_wait).until(
            EC.presence_of_element_located(locator)
        )

    def _find_visible_element(self, locator):
        return WebDriverWait(self.driver, self.default_wait).until(
            EC.visibility_of_element_located(locator)
        )

    def ai_find_element(self, description):
        locator_str = self.ai_finder.find_element_locator(self.driver, description)
        if not locator_str:
            raise NoSuchElementException(f"AI could not generate a locator for: '{description}'")

        print(f"AI generated XPath for '{description}': {locator_str}")

        try:
            return self._find_element((By.XPATH, locator_str))
        except TimeoutException:
            raise NoSuchElementException(
                f"AI-generated XPath '{locator_str}' did not find any element for: '{description}'")

    def ai_click(self, description):
        locator_str = self.ai_finder.find_element_locator(self.driver, description)
        if not locator_str:
            raise NoSuchElementException(f"AI could not generate a locator for clicking: '{description}'")

        print(f"AI generated XPath for clicking '{description}': {locator_str}")

        try:
            element = self._find_visible_element((By.XPATH, locator_str))
            element.click()
        except TimeoutException:
            raise NoSuchElementException(
                f"AI-generated XPath '{locator_str}' did not find a visible element to click for: '{description}'")

    def ai_type(self, description, text):
        locator_str = self.ai_finder.find_element_locator(self.driver, description)
        if not locator_str:
            raise NoSuchElementException(f"AI could not generate a locator for typing into: '{description}'")

        print(f"AI generated XPath for typing '{description}': {locator_str}")

        try:
            element = self._find_visible_element((By.XPATH, locator_str))
            element.clear()
            element.send_keys(text)
        except TimeoutException:
            raise NoSuchElementException(
                f"AI-generated XPath '{locator_str}' did not find a visible element to type into for: '{description}'")

    def wait_for_element_text(self, description, text_to_find, timeout=10):
        locator_str = self.ai_finder.find_element_locator(self.driver, description)
        if not locator_str:
            raise NoSuchElementException(f"AI could not generate a locator for waiting on text for: '{description}'")

        print(f"AI generated XPath for waiting on text for '{description}': {locator_str}")

        try:
            WebDriverWait(self.driver, timeout).until(
                EC.text_to_be_present_in_element((By.XPATH, locator_str), text_to_find)
            )
            return True
        except TimeoutException:
            return False

    def get_current_url(self):
        return self.driver.current_url

    def go_to(self, url):
        self.driver.get(url)