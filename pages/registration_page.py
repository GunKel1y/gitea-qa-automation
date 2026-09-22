import os

from pages.base_page import BasePage
from playwright.sync_api import Page, expect

class RegisterPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self._register_form = page.locator("//div[@class='ui attached segment']/form[@action='/user/sign_up']/..")
        self._username_field = page.locator('#user_name')
        self._email_field = page.locator('#email')
        self._password_field = page.locator('#password')
        self._doublecheck_password_field = page.locator('#retype')
        self._registration_button = page.get_by_text('Регистрация аккаунта')
        self._error_message = page.locator('div.negative.message.flash-message.flash-error')

    def open(self) -> None:
        self.page.goto(f"{os.getenv('BASE_URL_UI')}/user/sign_up")

    def registration_form_is_displayed(self) -> None:
        expect(self._register_form).to_be_visible()

    def fill_username(self, value: str) -> None:
        self._username_field.fill(value)

    def check_username_value(self, expected: str) -> None:
        expect(self._username_field).to_have_value(expected)

    def fill_email(self, value) -> None:
        self._email_field.fill(value)

    def check_email_value(self, expected: str) -> None:
        expect(self._email_field).to_have_value(expected)

    def fill_password(self, value) -> None:
        self._password_field.fill(value)

    def check_password_value(self, expected: str) -> None:
        expect(self._password_field).to_have_value(expected)

    def fill_doublecheck_password(self, value) -> None:
        self._doublecheck_password_field.fill(value)

    def check_doublecheck_password_value(self, expected: str) -> None:
        expect(self._doublecheck_password_field).to_have_value(expected)

    def click_registration_button(self) -> None:
        self._registration_button.click()

    def error_message_is_displayed(self) -> None:
        expect(self._error_message).to_be_visible()

    def check_error_message_text(self, expected_mgs: str) -> None:
        expect(self._error_message).to_have_text(expected_mgs)