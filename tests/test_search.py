import pytest
from framework.handlers.search import SearchHandler


@pytest.mark.skip(reason="Target site quotes.toscrape.com does not have a search feature")
@pytest.mark.smoke
def test_search_for_term(actions):
    search_handler = SearchHandler(actions)
    search_term = "smart watch"

    search_handler.search_for(search_term)

    results_text = search_handler.get_results_count_text()
    assert "results for" in results_text and search_term in results_text