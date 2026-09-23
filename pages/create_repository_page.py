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
        self._error_message = page.locator("div.negative.message.flash-message.flash-error")
        self._checkbox_private_repo = page.locator("input[name='private'][type='checkbox']")
        self._initialization_repo_checkbox = page.locator("input[name='auto_init'][type='checkbox']")
        self.gitignore_dropdown = SearchDropdown(page, "gitignores")

    def open(self) -> None:
        self.page.goto(f"{os.getenv("BASE_URL_UI")}/repo/create")

    def repo_name_field_is_displayed(self) -> None:
        expect(self._repo_name_field).to_be_visible()

    def fill_repo_name_field(self, value:str) -> None:
        self._repo_name_field.fill(value)

    def check_repo_name_field_value(self, value) -> None:
        expect(self._repo_name_field).to_have_value(value)

    def click_repo_create_button(self) -> None:
        self._create_repo_button.click()

    def create_repo_form_is_displayed(self) -> None:
        expect(self._create_repo_form).to_be_visible()

    def error_message_is_displayed(self) -> None:
        expect(self._error_message).to_be_visible()

    def check_negative_message_text(self, expected_mgs: str) -> None:
        expect(self._error_message).to_have_text(expected_mgs)

    def select_checkbox_private_repo(self):
        self._checkbox_private_repo.check()

    def verify_activated_checkbox_private_repo(self):
        expect(self._checkbox_private_repo).to_be_checked()

    def select_checkbox_initialization_repo(self):
        self._initialization_repo_checkbox.check()

    def verify_checkbox_activated_initialization_repo(self):
        expect(self._initialization_repo_checkbox).to_be_checked()