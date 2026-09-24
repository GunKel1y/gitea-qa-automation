import os

from components.search_dropdown import SearchDropdown
from pages.base_page import BasePage
from playwright.sync_api import Page, expect


class CreateRepositoryPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self._repo_name_field = page.locator("input#repo_name")
        self._create_repo_button = page.locator(
            "//div[@class='inline field']/button[contains(text(), 'Создать репозиторий')]"
        )
        self._create_repo_form = page.locator("form.new-repo-form[action='/repo/create']")
        self._checkbox_private_repo = page.locator("input[name='private'][type='checkbox']")
        self._initialization_repo_checkbox = page.locator("input[name='auto_init'][type='checkbox']")
        self.gitignore_dropdown = SearchDropdown(page, "gitignores")
        self.license_dropdown = SearchDropdown(page, "license")
        self._full_main_content = page.locator("div.full.height")
        self._default_branch_input = page.locator("#default_branch")

    def open(self) -> None:
        self.page.goto(f"{os.getenv("BASE_URL_UI")}/repo/create")

    def fill_repo_name_field(self, value:str) -> None:
        self._repo_name_field.fill(value)

    def click_repo_create_button(self) -> None:
        self._create_repo_button.click()

    def create_repo_form_is_displayed(self) -> None:
        expect(self._create_repo_form).to_be_visible()

    def select_checkbox_private_repo(self):
        self._checkbox_private_repo.check()

    def select_checkbox_initialization_repo(self):
        self._initialization_repo_checkbox.check()

    def press_esc(self):
        self._full_main_content.press("Escape")

    def fill_default_branch_field(self, value: str) -> None:
        self._default_branch_input.fill(value)