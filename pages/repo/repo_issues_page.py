import os

from playwright.sync_api import Page, Locator, expect

from pages.repo.base_repo_page import BaseRepoPage


class RepoIssuesPage(BaseRepoPage):

    def __init__(self, page: Page):
        super().__init__(page)
        self._new_issues_button = page.locator("a.issue-list-new")
        self._labels_dropdown = page.locator("div#issue-filters div.label-filter")

    def _labels_item(self, item: str) -> Locator:
        return self._labels_dropdown.locator("a").filter(has_text=item)

    def open(self, *, username: str, repo_name: str) -> None:
        self.page.goto(f"{os.getenv('GITEA_UI_URL')}/{username}/{repo_name}/issues")

    def click_new_issues_button(self) -> None:
        self._new_issues_button.click()

    def open_labels_dropdown(self) -> None:
        self._labels_dropdown.click()

    def labels_item_should_be_visible(self, item: str) -> None:
        expect(self._labels_item(item)).to_be_visible()