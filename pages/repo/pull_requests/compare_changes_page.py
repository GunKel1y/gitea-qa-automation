import re

from playwright.sync_api import Locator, Page, expect

from components.pull_requests_diff import PullRequestsDiff
from helpers.allure_helpers import step
from pages.repo.base_repo_page import BaseRepoPage


class CompareChangesPage(BaseRepoPage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.pr_diff = PullRequestsDiff(page)

        self._new_pr_button = page.locator("a[data-panel^='.pullrequest-form-toggle']")
        self._pr_title = page.locator("input#issue_title")
        self._comment_create_pr_button = page.locator("div.comment button.button")

        # ========== Локаторы дропдауна веток из которой тянутся изменения ==========
        self._dropdown_button_take_from_branch = page.locator(
            "//a//div[@class='compare-separator']//../following-sibling::div"
        )
        self._dropdown_container = self._dropdown_button_take_from_branch.locator("//div[@role='listbox']")
        self._dropdown_items_list = self._dropdown_container.locator("//div[contains(@class, 'head-branch-list')]")

        # ========== Локаторы блока коммитов ==========
        self._commits_header = page.locator("div h4.commits-table")
        self._count_commits_text = self._commits_header.locator("div.commits-table-left")
        self._base_branch = self._commits_header.locator("div.commits-table-right")

    def _dropdown_item(self, branch_name: str) -> Locator:
        return self._dropdown_items_list.locator(f"//a[contains(@href, '{branch_name}')]")

    @step('Проверить заголовок запроса на слияние. Ожидается: "{value}"')
    def check_pr_title_field_value(self, value: str) -> None:
        expect(self._pr_title).to_have_value(value)

    @step('Проверить ветки слияния в заголовке коммитов. Ожидаются: "{base_branch}, {take_from_branch}"')
    def check_commits_header_branches_text(self, *, base_branch: str, take_from_branch: str) -> None:
        branches = re.compile(rf"{base_branch}\s+.*\s+{take_from_branch}", re.DOTALL)
        expect(self._base_branch).to_contain_text(branches)

    @step('Нажать на кнопку выпадающего списка "Взять из:"')
    def click_take_from_branch_dropdown(self) -> None:
        self._dropdown_button_take_from_branch.click()

    @step('В выпадающем списке "Взять из:" выбрать пункт: "{branch_name}"')
    def select_dropdown_item(self, branch_name: str) -> None:
        self._dropdown_item(branch_name).click()

    @step('Проверить количество коммитов. Ожидается: "{count_commit}"')
    def check_commits_count(self, count_commit: int) -> None:
        expect(self._count_commits_text).to_have_text(f"{count_commit} Коммитов")

    @step('Нажать на кнопку "Новый запрос на слияние"')
    def click_new_pr_button(self) -> None:
        self._new_pr_button.click()

    @step('Нажать на кнопку "Создать запрос на слияние" в блоке комментария')
    def click_comment_create_pr_button(self) -> None:
        self._comment_create_pr_button.click()
