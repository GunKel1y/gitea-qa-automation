import os

from playwright.sync_api import Locator, Page, expect

from helpers.allure_helpers import step
from pages.repo.repo_page import RepoPage


class RepoCommitsBranchPage(RepoPage):
    def __init__(self, page: Page):
        super().__init__(page)
        self._commit_list_container = page.locator("//table[@id='commits-table']")

    def _sha_badge_in_commit_line(self, sha: str) -> Locator:
        return self._commit_list_container.locator(f"//td[@class='sha']//a[contains(@href, '{sha}')]")

    @step('Открыть страницу с информацией о коммитах ветки "{branch}"')
    def open(self, *, owner_repo: str, repo_name: str, branch: str) -> None:
        self.page.goto(f"{os.getenv('GITEA_UI_URL')}/{owner_repo}/{repo_name}/commits/branch/{branch}")

    @step('Проверить наличие коммита в списке коммитов ветки. Ожидается наличие коммита: "{sha}"')
    def check_sha_badge_in_branch_commits_list(self, sha: str) -> None:
        expect(self._sha_badge_in_commit_line(sha)).to_be_visible()
