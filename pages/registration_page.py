import os

from playwright.sync_api import Page, expect

from helpers.allure_helpers import step
from pages.base_page import BasePage


class RegisterPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self._register_form = page.locator("//div[@class='ui attached segment']/form[@action='/user/sign_up']/..")
        self._username_field = page.locator("#user_name")
        self._email_field = page.locator("#email")
        self._password_field = page.locator("#password")
        self._doublecheck_password_field = page.locator("#retype")
        self._registration_button = page.locator("form.ui.form[action='/user/sign_up'] button")

    @step("Открыть страницу регистрации")
    def open(self) -> None:
        self.page.goto(f"{os.getenv('GITEA_UI_URL')}/user/sign_up")

    @step("Проверить отображение формы регистрации")
    def check_registration_form_visible(self) -> None:
        expect(self._register_form).to_be_visible()

    @step('Ввести в поле "Имя пользователя" значение: "{value}"')
    def fill_username(self, value: str) -> None:
        self._username_field.fill(value)

    @step('Ввести в поле "Адрес электронной почты" значение: "{value}"')
    def fill_email(self, value) -> None:
        self._email_field.fill(value)

    @step('Ввести в поле "Пароль" значение', mask=["value"])
    def fill_password(self, value) -> None:
        self._password_field.fill(value)

    @step('Ввести в поле "Подтвердить пароль" значение', mask=["value"])
    def fill_doublecheck_password(self, value) -> None:
        self._doublecheck_password_field.fill(value)

    @step('Проверить значение поля "Подтвердить пароль"', mask=["expected"])
    def check_doublecheck_password_value(self, expected: str) -> None:
        expect(self._doublecheck_password_field).to_have_value(expected)

    @step('Нажать на кнопку "Регистрация аккаунта"')
    def click_registration_button(self) -> None:
        self._registration_button.click()

    @step('Проверить отображение нативной подсказки обязательности поля "Имя пользователя"')
    def check_username_required_hint_visible(self) -> None:
        expect(self._username_field.and_(self._invalid_fields)).to_have_count(1)

    @step('Проверить отображение нативной подсказки обязательности поля "Пароль"')
    def check_password_required_hint_visible(self) -> None:
        expect(self._password_field.and_(self._invalid_fields)).to_have_count(1)
