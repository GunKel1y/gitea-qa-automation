import os
import re

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
        self._create_commit_button = page.locator("div.merge-button button")

        # ========= Локаторы для блока коммита запроса на слияние =========
        self._pr_merge_commit_container = page.locator("div#pull-request-merge-form")
        self._pr_merge_commit_title = self._pr_merge_commit_container.locator("input[name='merge_title_field']")
        self._pr_merge_commit_description = self._pr_merge_commit_container.locator(
            "textarea[name='merge_message_field']"
        )
        self._pr_merge_commit_accept_button = self._pr_merge_commit_container.locator("button.button[value='merge']")

    @step('Открыть страницу запроса на слияние: "{owner_repo}/{repo_name}/{pr_index}"')
    def open(self, *, owner_repo: str, repo_name: str, pr_index: int) -> None:
        self.page.goto(f"{os.getenv('GITEA_UI_URL')}/{owner_repo}/{repo_name}/pulls/{pr_index}")

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

    @step('Нажать на кнопку "Создать коммит на слияние (дефолтное значение)"')
    def click_create_commit_button(self) -> None:
        self._create_commit_button.click()

    @step(
        "Проверить заголовок коммита слияния. Ожидается: "
        '"Merge pull request "{pr_title}" ({pr_index}) from {head_branch} into {base_branch}"'
    )
    def check_pr_merge_commit_title_value(
        self, pr_title: str, pr_index: str, head_branch: str, base_branch: str
    ) -> None:
        expected_title = f"Merge pull request '{pr_title}' ({pr_index}) from {head_branch} into {base_branch}"
        expect(self._pr_merge_commit_title).to_have_value(expected_title)

    @step("Проверить описание коммита слияния. Ожидается: Reviewed-on: /{owner_repo}/{repo_name}/pulls/{pr_index}")
    def check_pr_merge_commit_description_value(self, owner_repo: str, repo_name: str, pr_index: int) -> None:
        expected_description = re.compile(
            rf"^Reviewed-on: {os.getenv('GITEA_UI_URL')}/{owner_repo}/{repo_name}/pulls/{pr_index}\s*$"
        )
        expect(self._pr_merge_commit_description).to_have_value(expected_description)

    @step('Нажать на кнопку "Создать коммит на слияние" в блоке коммита')
    def click_pr_merge_commit_accept_button(self) -> None:
        # Gitea отклоняет слияние, пока PR после создания в статусе "checking" (на UI этого не видно)
        self.page.wait_for_timeout(3000)
        self._pr_merge_commit_accept_button.click()
