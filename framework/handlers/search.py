from selenium.common.exceptions import NoSuchElementException

class SearchHandler:
    def __init__(self, actions):
        self.actions = actions

    def search_for(self, term):
        self.actions.ai_type("the main search bar", term)
        self.actions.ai_click("the search submit button")

    def get_results_count_text(self):
        try:
            element = self.actions.ai_find_element("the text indicating number of search results")
            return element.text
        except NoSuchElementException:
            return "0 results found"