import pytest
from framework.handlers.navigation import NavigationHandler


@pytest.mark.smoke
def test_navigate_by_tag(actions):
    nav_handler = NavigationHandler(actions)
    tag_to_click = "love"
    nav_handler.go_to_menu_item(tag_to_click)

    assert f"/tag/{tag_to_click}" in actions.get_current_url()
    assert actions.wait_for_element_text("the page title heading", "love", timeout=5)


@pytest.mark.regression
def test_pagination(actions):
    nav_handler = NavigationHandler(actions)

    first_page_quote = actions.ai_find_element("the first quote text on the page").text

    nav_handler.click_next_page()

    second_page_quote = actions.ai_find_element("the first quote text on the page").text

    assert first_page_quote != second_page_quote, "Content did not change after clicking next page"