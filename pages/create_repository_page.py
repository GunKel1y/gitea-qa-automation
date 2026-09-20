import os

from pages.base_page import BasePage
from playwright.sync_api import Page, expect

class CreateRepositoryPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.__REPO_NAME_FIELD = page.locator("input#repo_name")
        self.__CREATE_REPO_BUTTON = page.locator(
            "//div[@class='inline field']/button[contains(text(), 'Создать репозиторий')]"
        )
        self.__CREATE_REPO_FORM = page.locator("form.new-repo-form[action='/repo/create']")

    def open(self):
        self.page.goto(f"{os.getenv("BASE_URL_UI")}/repo/create")

    def repo_name_field_is_displayed(self) -> None:
        expect(self.__REPO_NAME_FIELD).to_be_visible()

    def fill_repo_name_field(self, value:str) -> None:
        self.__REPO_NAME_FIELD.fill(value)

    def check_repo_name_field_value(self, value):
        expect(self.__REPO_NAME_FIELD).to_have_value(value)

    def click_repo_create_button(self):
        self.__CREATE_REPO_BUTTON.click()

    def create_repo_form_is_displayed(self):
        expect(self.__CREATE_REPO_FORM).to_be_visible()