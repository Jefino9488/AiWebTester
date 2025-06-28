class NavigationHandler:
    def __init__(self, actions):
        self.actions = actions

    def go_to_menu_item(self, menu_item_text):
        self.actions.ai_click(f"the navigation link for '{menu_item_text}'")

    def click_next_page(self):
        self.actions.ai_click("the 'Next' button for pagination")