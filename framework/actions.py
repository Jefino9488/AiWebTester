from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time


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
        element = self.ai_find_element(description)
        element.clear()
        element.send_keys(text)

    def ai_hover(self, description):
        """Hover over an element found using AI."""
        element = self.ai_find_element(description)
        ActionChains(self.driver).move_to_element(element).perform()

    def ai_double_click(self, description):
        """Double click on an element found using AI."""
        element = self.ai_find_element(description)
        ActionChains(self.driver).double_click(element).perform()

    def ai_right_click(self, description):
        """Right click on an element found using AI."""
        element = self.ai_find_element(description)
        ActionChains(self.driver).context_click(element).perform()

    def ai_drag_and_drop(self, source_description, target_description):
        """Drag and drop from source to target elements found using AI."""
        source = self.ai_find_element(source_description)
        target = self.ai_find_element(target_description)
        ActionChains(self.driver).drag_and_drop(source, target).perform()

    def ai_scroll_to(self, description):
        """Scroll to an element found using AI."""
        element = self.ai_find_element(description)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        # Small pause to allow any dynamic content to load
        time.sleep(0.5)

    def ai_wait_until_visible(self, description, timeout=None):
        """Wait until an element is visible using AI-generated locator."""
        timeout = timeout or self.default_wait
        locator_str = self.ai_finder.find_element_locator(self.driver, description)
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((By.XPATH, locator_str))
            )
        except TimeoutException:
            raise TimeoutException(f"Element '{description}' did not become visible within {timeout} seconds")

    def ai_wait_until_clickable(self, description, timeout=None):
        """Wait until an element is clickable using AI-generated locator."""
        timeout = timeout or self.default_wait
        locator_str = self.ai_finder.find_element_locator(self.driver, description)
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((By.XPATH, locator_str))
            )
        except TimeoutException:
            raise TimeoutException(f"Element '{description}' did not become clickable within {timeout} seconds")

    def ai_select_option(self, dropdown_description, option_description):
        """Select an option from a dropdown using AI."""
        dropdown = self.ai_find_element(dropdown_description)
        dropdown.click()
        option = self.ai_find_element(option_description)
        option.click()

    def ai_get_text(self, description):
        """Get text from an element found using AI."""
        element = self.ai_find_element(description)
        return element.text

    def ai_get_attribute(self, description, attribute):
        """Get attribute value from an element found using AI."""
        element = self.ai_find_element(description)
        return element.get_attribute(attribute)

    def ai_is_displayed(self, description):
        """Check if an element found using AI is displayed."""
        try:
            element = self.ai_find_element(description)
            return element.is_displayed()
        except NoSuchElementException:
            return False

    def ai_is_enabled(self, description):
        """Check if an element found using AI is enabled."""
        element = self.ai_find_element(description)
        return element.is_enabled()

    def ai_press_key(self, description, key):
        """Press a specific key in an element found using AI."""
        element = self.ai_find_element(description)
        element.send_keys(getattr(Keys, key.upper()))

    def ai_clear_and_type(self, description, text):
        """Clear and type text in an element found using AI."""
        element = self.ai_find_element(description)
        element.clear()
        # Small pause to ensure field is cleared
        time.sleep(0.1)
        element.send_keys(text)

    def ai_submit_form(self, form_description):
        """Submit a form found using AI."""
        form = self.ai_find_element(form_description)
        form.submit()

    def ai_find_elements(self, description):
        """Find multiple elements using AI."""
        locator_str = self.ai_finder.find_element_locator(self.driver, description)
        return self.driver.find_elements(By.XPATH, locator_str)

    def ai_click_if_exists(self, description, timeout=5):
        """Click an element if it exists within the specified timeout."""
        try:
            element = self.ai_wait_until_clickable(description, timeout)
            element.click()
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def get_current_url(self):
        return self.driver.current_url

    def go_to(self, url):
        self.driver.get(url)