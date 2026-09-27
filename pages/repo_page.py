import os

from pages.base_page import BasePage
from playwright.sync_api import Page, expect, Locator


class RepoPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self._empty_repo_guide = page.locator("div.content>div.empty-repo-guide")
        self._privacy_status = page.locator("div.flex-item-trailing>span.not-mobile")
        self._readme_content = page.locator("div#readme")
        self._branch_dropdown_button = page.locator("div.custom.branch-selector-dropdown")
        self._branch_text_in_dropdown = page.locator("span.gt-ellipsis>strong.gt-ellipsis")

    def _repo_name_in_header(self, *, username: str, repo_name: str) -> Locator:
        return self.page.locator(f"a.muted[href='/{username}/{repo_name}']")

    def open(self, *, username: str, repo_name: str) -> None:
        self.page.goto(f"{os.getenv('BASE_URL_UI')}/{username}/{repo_name}")

    def empty_repo_guide_is_displayed(self) -> None:
        expect(self._empty_repo_guide).to_be_visible()

    def repo_name_in_header_is_displayed(self, *, username: str, repo_name: str) -> None:
        expect(self._repo_name_in_header(username=username, repo_name=repo_name)).to_be_visible()

    def privacy_status_is_displayed(self) -> None:
        expect(self._privacy_status).to_be_visible()

    def readme_content_is_displayed(self) -> None:
        expect(self._readme_content).to_be_visible()

    def specified_file_in_list(self, file: str) -> None:
        expect(self.page.locator(f"div.repo-file-cell.name>a.entry-name[title='{file}']")).to_be_visible()

    def branch_dropdown_button_is_displayed(self) -> None:
        expect(self._branch_dropdown_button).to_be_visible()

    def check_branch_dropdown_button_text(self, value: str) -> None:
        expect(self._branch_text_in_dropdown).to_have_text(value)