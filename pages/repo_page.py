import os

from pages.base_page import BasePage
from playwright.sync_api import Page, expect, Locator


class RepoPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self._empty_repo_guide = page.locator("div.content>div.empty-repo-guide")

    def _repo_name_in_header(self, *, username: str, repo_name: str) -> Locator:
        return self.page.locator(f"a.muted[href='/{username}/{repo_name}']")

    def open(self, *, username: str, repo_name: str) -> None:
        self.page.goto(f"{os.getenv('BASE_URL_UI')}/{username}/{repo_name}")

    def empty_repo_guide_is_displayed(self) -> None:
        expect(self._empty_repo_guide).to_be_visible()

    def repo_name_in_header_is_displayed(self, *, username: str, repo_name: str) -> None:
        expect(self._repo_name_in_header(username=username, repo_name=repo_name)).to_be_visible()