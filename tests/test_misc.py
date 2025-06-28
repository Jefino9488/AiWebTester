import pytest
from framework.handlers.misc import MiscHandler


@pytest.mark.skip(reason="Target site does not have checkboxes for this test")
@pytest.mark.regression
def test_checkbox_interaction(actions):
    misc_handler = MiscHandler(actions)

    actions.ai_click("the 'Products' page link")

    checkbox_label = "In Stock Only"
    misc_handler.check_checkbox_by_label(checkbox_label)

    assert True


@pytest.mark.skip(reason="Target site does not have dropdowns for this test")
@pytest.mark.regression
def test_dropdown_selection(actions):
    misc_handler = MiscHandler(actions)

    actions.ai_click("the 'All Products' category")

    dropdown_desc = "the sort by dropdown"
    option_to_select = "Price: High to Low"
    misc_handler.select_dropdown_option(dropdown_desc, option_to_select)

    assert True