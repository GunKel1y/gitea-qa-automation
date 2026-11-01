import os

from playwright.sync_api import Locator, Page, expect

from components.search_dropdown import SearchDropdown
from helpers.allure_helpers import step
from pages.repo.base_repo_page import BaseRepoPage


class CreateRepositoryPage(BaseRepoPage):
    def __init__(self, page: Page):
        super().__init__(page)
        self._repo_name_field = page.locator("input#repo_name")
        self._create_repo_button = page.locator("form.new-repo-form button")
        self._create_repo_form = page.locator("form.new-repo-form[action='/repo/create']")
        self._repo_description = page.locator("#description")
        self._checkbox_private_repo = page.locator("input[name='private'][type='checkbox']")
        self._initialization_repo_checkbox = page.locator("input[name='auto_init'][type='checkbox']")
        self.gitignore_dropdown = SearchDropdown(page, "gitignores", name="Gitignore")
        self.license_dropdown = SearchDropdown(page, "license", name="Лицензия")
        self.repo_template = SearchDropdown(page, "repo_template", name="Шаблон репозитория")
        self.issue_labels = SearchDropdown(page, "issue_labels", name="Метки задач")
        self._full_main_content = page.locator("div.full.height")
        self._default_branch_input = page.locator("#default_branch")
        self._owner_field = page.locator("#repo_owner_dropdown")
        self._checkbox_git_content = page.locator("input[name='git_content']")
        self._checkbox_labels = page.locator("input[name='labels']")

    def _owner_menu_item(self, owner: str) -> Locator:
        return self.page.locator(f"#repo_owner_dropdown>div.menu>div[title='{owner}']")

    @step("Открыть страницу создания репозитория")
    def open(self) -> None:
        self.page.goto(f"{os.getenv('GITEA_UI_URL')}/repo/create")

    @step('Ввести в поле "Название репозитория" значение: "{value}"')
    def fill_repo_name_field(self, value: str) -> None:
        self._repo_name_field.fill(value)

    @step('Нажать на кнопку "Создать репозиторий"')
    def click_repo_create_button(self) -> None:
        self._create_repo_button.click()

    @step("Проверить отображение формы создания репозитория")
    def check_create_repo_form_visible(self) -> None:
        expect(self._create_repo_form).to_be_visible()

    @step('Отметить чекбокс "Сделать репозиторий приватным"')
    def select_checkbox_private_repo(self):
        self._checkbox_private_repo.check()

    @step('Отметить чекбокс "Инициализировать репозиторий"')
    def select_checkbox_initialization_repo(self):
        self._initialization_repo_checkbox.check()

    @step('Нажать клавишу "Esc"')
    def press_esc(self):
        """Закрывает открытый выпадающий список"""
        self._full_main_content.press("Escape")

    @step('Ввести в поле "Ветка по умолчанию" значение: "{value}"')
    def fill_default_branch_field(self, value: str) -> None:
        self._default_branch_input.fill(value)

    @step('Открыть выпадающий список "Владелец"')
    def owner_field_click(self) -> None:
        self._owner_field.click()

    @step('Выбрать владельца: "{owner}"')
    def select_owner(self, owner: str) -> None:
        self._owner_menu_item(owner).click()

    @step('Проверить доступность выбора владельца: "{owner}"')
    def check_owner_selectable(self, owner: str) -> None:
        expect(self._owner_menu_item(owner)).to_be_visible()

    @step('Проверить недоступность выбора владельца: "{owner}"')
    def check_owner_not_selectable(self, owner: str) -> None:
        expect(self._owner_menu_item(owner)).not_to_be_visible()

    @step('Ввести в поле "Описание" значение: "{text}"')
    def fill_repo_description(self, text: str) -> None:
        self._repo_description.fill(text)

    @step('Проверить значение описания репозитория. Ожидается: "{text}"')
    def check_repo_description_value(self, text: str) -> None:
        expect(self._repo_description).to_have_value(text)

    @step('Отметить чекбокс "Содержимое Git" в блоке "Элементы шаблона"')
    def select_checkbox_git_content(self) -> None:
        self._checkbox_git_content.check()

    @step('Отметить чекбокс "Метки задач" в блоке "Элементы шаблона"')
    def select_checkbox_labels_issues(self) -> None:
        self._checkbox_labels.check()
