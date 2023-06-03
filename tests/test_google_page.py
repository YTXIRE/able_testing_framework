from core.allure_wrapper import allure_wrapper


class TestGoogleSearchPage:
    @allure_wrapper(
        allure_title="Checking the Google search page",
        allure_suite="Checking the Google search page",
        allure_parent_suite="Checking the Google search page",
        test_case_id=1,
    )
    def test_google_search(self, google_page):
        google_page.open()
        google_page.fill_search_form('Тест')
        google_page.click_button()
        google_page.should_be_visible_results_search()
