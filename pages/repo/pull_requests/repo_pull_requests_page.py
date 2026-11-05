import os

from playwright.sync_api import Page

from helpers.allure_helpers import step
from pages.repo.base_repo_page import BaseRepoPage


class RepoPullRequestsPage(BaseRepoPage):
    def __init__(self, page: Page):
        super().__init__(page)
        self._new_pull_request_button = page.locator("div.list-header a.new-pr-button")

    @step('Открыть страницу запросов на слияние в репозитории "{repo_owner}/{repo_name}"')
    def open(self, *, repo_owner: str, repo_name: str) -> None:
        self.page.goto(f"{os.getenv('GITEA_UI_URL')}/{repo_owner}/{repo_name}/pulls")

    @step('Нажать на кнопку "Новый запрос на слияние"')
    def click_new_pr_button(self) -> None:
        self._new_pull_request_button.click()
