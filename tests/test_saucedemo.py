import pytest
import time


@pytest.mark.regression
class TestSauceDemoSimulation:

    @pytest.fixture(autouse=True)
    def setup(self, actions, cfg):
        self.actions = actions
        self.cfg = cfg

    def handle_post_login_alert(self):
        try:
            self.actions.ai_click_if_exists("the alert accept button", timeout=2)
        except:
            pass

    @pytest.mark.usefixtures("actions", "cfg")
    def test_login_and_add_to_cart(self):
        creds = self.cfg['target_site']['credentials']['valid_user']
        self.actions.ai_clear_and_type("the username input field", creds['username'])
        self.actions.ai_clear_and_type("the password input field", creds['password'])
        self.actions.ai_click("the login button")
        self.handle_post_login_alert()

        assert 'inventory.html' in self.actions.get_current_url(), "Not redirected to inventory page after login"

        self.actions.ai_click("the add to cart button for Sauce Labs Backpack")
        self.actions.ai_click("the add to cart button for Sauce Labs Onesie")

        self.actions.ai_click("the shopping cart link")

        backpack_item = self.actions.ai_is_displayed("the cart item named Sauce Labs Backpack")
        onesie_item = self.actions.ai_is_displayed("the cart item named Sauce Labs Onesie")
        assert backpack_item, "Backpack not found in cart"
        assert onesie_item, "Onesie not found in cart"

    @pytest.mark.usefixtures("actions", "cfg")
    def test_sidebar_navigation(self):
        creds = self.cfg['target_site']['credentials']['valid_user']
        self.actions.ai_clear_and_type("the username input field", creds['username'])
        self.actions.ai_clear_and_type("the password input field", creds['password'])
        self.actions.ai_click("the login button")
        self.handle_post_login_alert()

        self.actions.ai_click("the burger menu button")
        original_window = self.actions.driver.current_window_handle

        self.actions.ai_click("the About link")

        time.sleep(1)
        for handle in self.actions.driver.window_handles:
            if handle != original_window:
                self.actions.driver.switch_to.window(handle)
                break

        current_url = self.actions.get_current_url()
        assert "saucelabs.com" in current_url, f"Expected URL to contain 'saucelabs.com', got {current_url}"

    @pytest.mark.usefixtures("actions", "cfg")
    def test_cart_persistence_on_refresh(self):
        creds = self.cfg['target_site']['credentials']['valid_user']
        self.actions.ai_clear_and_type("the username input field", creds['username'])
        self.actions.ai_clear_and_type("the password input field", creds['password'])
        self.actions.ai_click("the login button")
        self.handle_post_login_alert()

        self.actions.ai_click("the add to cart button for Sauce Labs Bike Light")

        cart_badge = self.actions.ai_get_text("the shopping cart badge")
        assert cart_badge == "1", f"Expected cart count to be 1, got {cart_badge}"

        self.actions.driver.refresh()

        cart_badge_after = self.actions.ai_get_text("the shopping cart badge")
        assert cart_badge_after == "1", "Cart count didn't persist after refresh"
