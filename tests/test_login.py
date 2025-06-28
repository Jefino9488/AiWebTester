import pytest
from framework.handlers.login import LoginHandler


@pytest.mark.smoke
def test_successful_login(actions, cfg):
    login_handler = LoginHandler(actions, cfg)
    creds = cfg['target_site']['credentials']['valid_user']
    login_handler.login(creds['username'], creds['password'])

    logout_text = login_handler.get_logout_link_text()
    assert logout_text is not None, "Logout link not found after login"


@pytest.mark.regression
def test_failed_login(actions, cfg):
    login_handler = LoginHandler(actions, cfg)
    creds = cfg['target_site']['credentials']['invalid_user']
    login_handler.login(creds['username'], creds['password'])

    error_message = login_handler.get_error_message()
    assert error_message is not None, "Error message not found after failed login"
    assert "Invalid user name or password" in error_message, f"Unexpected error message: '{error_message}'"