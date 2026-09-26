from playwright.sync_api import Page

from pages.repo.base_repo_page import BaseRepoPage


class NewIssuesPage(BaseRepoPage):

    def __init__(self, page: Page):
        super().__init__(page)
        self._input_issue_title = page.locator("input#issue_title")
        self._add_issue_button = page.locator("div.content>div.tw-justify-end>button")

    def fill_input_issue_title(self, value: str) -> None:
        self._input_issue_title.fill(value)

    def click_add_issue_button(self):
        self._add_issue_button.click()