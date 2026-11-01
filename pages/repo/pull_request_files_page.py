import os

from playwright.sync_api import Page

from components.pull_requests_diff import PullRequestsDiff
from helpers.allure_helpers import step
from pages.repo.base_repo_page import BaseRepoPage


class PullRequestFilesPage(BaseRepoPage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.pr_diff = PullRequestsDiff(page)

    @step('Открыть вкладку с изменениями файлов в запросе на слияние "{owner_repo}/{repo_name}/{pr_index}"')
    def open(self, *, owner_repo: str, repo_name: str, pr_index: int) -> None:
        self.page.goto(f"{os.getenv('GITEA_UI_URL')}/{owner_repo}/{repo_name}/pulls/{pr_index}/files")