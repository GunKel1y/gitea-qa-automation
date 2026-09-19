import os

from pages.base_page import BasePage
from playwright.sync_api import Page, expect

class RegisterPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.__REGISTER_FORM = page.locator("//div[@class='ui attached segment']/form[@action='/user/sign_up']/..")
        self.__USERNAME_FIELD = page.locator('#user_name')
        self.__EMAIL_FIELD = page.locator('#email')
        self.__PASSWORD_FIELD = page.locator('#password')
        self.__DOUBLECHECK_PASSWORD_FIELD = page.locator('#retype')
        self.__REGISTRATION_BUTTON = page.get_by_text('Регистрация аккаунта')
        self.__ERROR_MESSAGE = page.locator('div.negative.message.flash-message.flash-error')

    def open(self):
        self.page.goto(f"{os.getenv('BASE_URL_UI')}/user/sign_up")

    def registration_form_is_displayed(self) -> None:
        expect(self.__REGISTER_FORM).to_be_visible()

    def fill_username(self, value: str) -> None:
        self.__USERNAME_FIELD.fill(value)

    def check_username_value(self, expected: str) -> None:
        expect(self.__USERNAME_FIELD).to_have_value(expected)

    def fill_email(self, value) -> None:
        self.__EMAIL_FIELD.fill(value)

    def check_email_value(self, expected: str) -> None:
        expect(self.__EMAIL_FIELD).to_have_value(expected)

    def fill_password(self, value) -> None:
        self.__PASSWORD_FIELD.fill(value)

    def check_password_value(self, expected: str) -> None:
        expect(self.__PASSWORD_FIELD).to_have_value(expected)

    def fill_doublecheck_password(self, value) -> None:
        self.__DOUBLECHECK_PASSWORD_FIELD.fill(value)

    def check_doublecheck_password_value(self, expected: str) -> None:
        expect(self.__DOUBLECHECK_PASSWORD_FIELD).to_have_value(expected)

    def click_registration_button(self) -> None:
        self.__REGISTRATION_BUTTON.click()

    def check_url(self, expected: str) -> None:
        expect(self.page).to_have_url(expected)

    def error_message_is_displayed(self) -> None:
        expect(self.__ERROR_MESSAGE).to_be_visible()

    def check_error_message_text(self, expected_mgs: str) -> None:
        expect(self.__ERROR_MESSAGE).to_have_text(expected_mgs)