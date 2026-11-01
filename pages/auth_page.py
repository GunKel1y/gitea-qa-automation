import os

from playwright.sync_api import Page, expect

from helpers.allure_helpers import step
from pages.base_page import BasePage


class AuthPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self._auth_form = page.locator("//div[@class='ui attached segment']/form[@action='/user/login']/..")
        self._username_field = page.locator("input#user_name")
        self._password_field = page.locator("input#password")
        self._login_button = page.locator("button.ui.primary.button")

    @step("Открыть страницу входа")
    def open(self) -> None:
        self.page.goto(f"{os.getenv('GITEA_UI_URL')}/user/login")

    @step("Проверить отображение формы входа")
    def check_auth_form_visible(self) -> None:
        expect(self._auth_form).to_be_visible()

    @step('Ввести в поле "Имя пользователя/Адрес эл.почты" значение: "{value}"')
    def fill_username(self, value: str) -> None:
        self._username_field.fill(value)

    @step('Ввести в поле "Пароль" значение', mask=["value"])
    def fill_password(self, value: str) -> None:
        self._password_field.fill(value)

    @step('Нажать на кнопку "Вход"')
    def click_login_button(self) -> None:
        self._login_button.click()
