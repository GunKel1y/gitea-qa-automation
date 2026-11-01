from playwright.sync_api import Page, expect

from helpers.allure_helpers import step
from pages.repo.base_repo_page import BaseRepoPage


class PullRequestPage(BaseRepoPage):
    def __init__(self, page: Page):
        super().__init__(page)
        self._pr_title = page.locator("div.issue-title>h1")
        self._pr_id = page.locator("div.issue-title>h1>span.index")
        self._pr_status_label = page.locator("div.issue-state-label")
        self._diff_files_tab = page.locator(
            "//div[contains(@class, 'pull tabs container')]//a[contains(@href,'files')]"
        )

    @step("Получить номер запроса на слияние")
    def get_pr_id(self) -> str:
        """Возвращает номер запроса на слияние вместе с "#" """
        return self._pr_id.inner_text()

    @step('Проверить заголовок запроса на слияние. Ожидается: "{expected_title} {expected_id}"')
    def check_pr_title_value(self, *, expected_title: str, expected_id: str) -> None:
        full_expected_text = f"{expected_title} {expected_id}"
        expect(self._pr_title).to_have_text(full_expected_text)

    @step('Проверить статус запроса на слияние. Ожидается: "{status_text}"')
    def check_pr_status_label_text(self, status_text: str) -> None:
        expect(self._pr_status_label).to_have_text(status_text)

    @step('Перейти во вкладку "Изменённые файлы"')
    def open_diff_files_tab(self) -> None:
        self._diff_files_tab.click()
