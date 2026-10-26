from playwright.sync_api import Locator, Page, expect


class RepoHeader:
    def __init__(self, page: Page):
        self.page = page
        self._created_by_repo_text = page.locator("div.fork-flag")

    def _repo_name_in_header(self, *, username: str, repo_name: str) -> Locator:
        return self.page.locator(f"a.muted[href='/{username}/{repo_name}']")

    def repo_name_in_header_is_displayed(self, *, username: str, repo_name: str) -> None:
        expect(self._repo_name_in_header(username=username, repo_name=repo_name)).to_be_visible()

    def check_created_by_repo_text(self, *, owner_template: str, repo_template: str) -> None:
        expect(self._created_by_repo_text).to_have_text(f"создано из {owner_template}/{repo_template}")
