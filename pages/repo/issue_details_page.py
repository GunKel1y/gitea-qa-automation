import re

from playwright.sync_api import Page, expect

from pages.repo.base_repo_page import BaseRepoPage


class IssueDetailsPage(BaseRepoPage):

    def __init__(self, page: Page):
        super().__init__(page)
        self._issue_title = page.locator("div.issue-title>h1")
        self._issue_id = page.locator("div.issue-title>h1>span.index")
        self._issue_status_label = page.locator("div.issue-state-label")

    def get_issue_id(self) -> str:
        return self._issue_id.inner_text()

    def issue_title_is_displayed(self) -> None:
        expect(self._issue_title).to_be_visible()

    def check_issue_title_value(self, expected_title_with_id: str) -> None:
        expect(self._issue_title).to_have_text(expected_title_with_id)

    def check_issue_status_label_text(self, status_text: str) -> None:
        expect(self._issue_status_label).to_have_text(status_text)