import os

from playwright.sync_api import Locator, Page, expect

from helpers.allure_helpers import step
from pages.repo.base_repo_page import BaseRepoPage


class RepoIssuesPage(BaseRepoPage):
    def __init__(self, page: Page):
        super().__init__(page)
        self._new_issues_button = page.locator("a.issue-list-new")
        self._labels_dropdown = page.locator("div#issue-filters div.label-filter")

    def _labels_item(self, item: str) -> Locator:
        return self._labels_dropdown.locator("a").filter(has_text=item)

    @step("Открыть список задач репозитория {username}/{repo_name}")
    def open(self, *, username: str, repo_name: str) -> None:
        self.page.goto(f"{os.getenv('GITEA_UI_URL')}/{username}/{repo_name}/issues")

    @step("Нажать кнопку создания новой задачи")
    def click_new_issues_button(self) -> None:
        self._new_issues_button.click()

    @step("Открыть фильтр по меткам")
    def open_labels_dropdown(self) -> None:
        self._labels_dropdown.click()

    @step("Проверить, что метка {item} есть в фильтре")
    def labels_item_should_be_visible(self, item: str) -> None:
        expect(self._labels_item(item)).to_be_visible()
