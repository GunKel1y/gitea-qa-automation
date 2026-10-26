import os

from playwright.sync_api import Locator, Page, expect

from components.search_dropdown import SearchDropdown
from pages.repo.base_repo_page import BaseRepoPage


class CreateRepositoryPage(BaseRepoPage):
    def __init__(self, page: Page):
        super().__init__(page)
        self._repo_name_field = page.locator("input#repo_name")
        self._create_repo_button = page.locator(
            "//div[@class='inline field']/button[contains(text(), 'Создать репозиторий')]"
        )
        self._create_repo_form = page.locator("form.new-repo-form[action='/repo/create']")
        self._repo_description = page.locator("#description")
        self._checkbox_private_repo = page.locator("input[name='private'][type='checkbox']")
        self._initialization_repo_checkbox = page.locator("input[name='auto_init'][type='checkbox']")
        self.gitignore_dropdown = SearchDropdown(page, "gitignores")
        self.license_dropdown = SearchDropdown(page, "license")
        self.repo_template = SearchDropdown(page, "repo_template")
        self.issue_labels = SearchDropdown(page, "issue_labels")
        self._full_main_content = page.locator("div.full.height")
        self._default_branch_input = page.locator("#default_branch")
        self._owner_field = page.locator("#repo_owner_dropdown")
        self._checkbox_git_content = page.locator("input[name='git_content']")
        self._checkbox_labels = page.locator("input[name='labels']")

    def _owner_menu_item(self, owner: str) -> Locator:
        return self.page.locator(f"#repo_owner_dropdown>div.menu>div[title='{owner}']")

    def open(self) -> None:
        self.page.goto(f"{os.getenv('GITEA_UI_URL')}/repo/create")

    def fill_repo_name_field(self, value: str) -> None:
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

    def owner_field_click(self) -> None:
        self._owner_field.click()

    def select_owner(self, owner: str) -> None:
        self._owner_menu_item(owner).click()

    def owner_is_selectable(self, owner: str) -> None:
        expect(self._owner_menu_item(owner)).to_be_visible()

    def owner_is_not_selectable(self, owner: str) -> None:
        expect(self._owner_menu_item(owner)).not_to_be_visible()

    def fill_repo_description(self, text: str) -> None:
        self._repo_description.fill(text)

    def repo_description_value_should_be_equal(self, text: str) -> None:
        expect(self._repo_description).to_have_value(text)

    def select_checkbox_git_content(self) -> None:
        self._checkbox_git_content.check()

    def select_checkbox_labels_issues(self) -> None:
        self._checkbox_labels.check()
