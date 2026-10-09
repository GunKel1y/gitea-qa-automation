import os

from playwright.sync_api import Page

from pages.repo.base_repo_page import BaseRepoPage


class RepoIssuesPage(BaseRepoPage):

    def __init__(self, page: Page):
        super().__init__(page)
        self._new_issues_button = page.locator("a.issue-list-new")

    def open(self, *, username: str, repo_name: str) -> None:
        self.page.goto(f"{os.getenv('GITEA_UI_URL')}/{username}/{repo_name}/issues")

    def click_new_issues_button(self):
        self._new_issues_button.click()