
from playwright.sync_api import Page, Locator, expect


class RepoHeader:
    
    def __init__(self, page: Page):
        self.page = page

    def _repo_name_in_header(self, *, username: str, repo_name: str) -> Locator:
        return self.page.locator(f"a.muted[href='/{username}/{repo_name}']")
    
    def repo_name_in_header_is_displayed(self, *, username: str, repo_name: str) -> None:
        expect(self._repo_name_in_header(username=username, repo_name=repo_name)).to_be_visible()
    
    