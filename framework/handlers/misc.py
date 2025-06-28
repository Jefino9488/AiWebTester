class MiscHandler:
    def __init__(self, actions):
        self.actions = actions

    def check_checkbox_by_label(self, label_text):
        self.actions.ai_click(f"the checkbox with the label '{label_text}'")

    def select_dropdown_option(self, dropdown_description, option_text):
        self.actions.ai_click(f"the dropdown menu for '{dropdown_description}'")
        self.actions.ai_click(f"the dropdown option '{option_text}'")