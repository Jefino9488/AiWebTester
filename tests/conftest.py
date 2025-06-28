import pytest
from framework.config_loader import load_config
from framework.driver_manager import get_driver
from framework.ai_finder import AiFinder
from framework.actions import Actions
from framework.utils import take_screenshot


@pytest.fixture(scope="session")
def cfg():
    return load_config()


@pytest.fixture(scope="session")
def ai_finder(cfg):
    if cfg['gemini']['api_key'] == "YOUR_GEMINI_API_KEY":
        pytest.skip("Gemini API key not configured. Skipping AI-based tests.")
    return AiFinder(cfg)


@pytest.fixture(scope="function")
def driver(cfg, request):
    driver_instance = get_driver(cfg)
    driver_instance.get(cfg['target_site']['base_url'])

    yield driver_instance

    if request.node.rep_call.failed:
        take_screenshot(driver_instance, request.node.name)

    driver_instance.quit()


@pytest.fixture(scope="function")
def actions(driver, ai_finder, cfg):
    return Actions(driver, ai_finder, cfg['webdriver']['implicit_wait'])


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)