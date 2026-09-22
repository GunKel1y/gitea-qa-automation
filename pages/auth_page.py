import os

from pages.base_page import BasePage
from playwright.sync_api import Page, expect


class AuthPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self._auth_form = page.locator("//div[@class='ui attached segment']/form[@action='/user/login']/..")
        self._username_field = page.locator("input#user_name")
        self._password_field = page.locator("input#password")
        self._login_button = page.locator("button.ui.primary.button")
        self._error_message = page.locator("div.negative.message.flash-message.flash-error")

    def open(self) -> None:
        self.page.goto(f"{os.getenv('BASE_URL_UI')}/user/login")

    def auth_form_is_displayed(self) -> None:
        expect(self._auth_form).to_be_visible()

    def fill_username(self, value: str) -> None:
        self._username_field.fill(value)

    def check_value_username(self, value: str) -> None:
        expect(self._username_field).to_have_value(value)

    def fill_password(self, value: str) -> None:
        self._password_field.fill(value)

    def check_value_password(self, value: str) -> None:
        expect(self._password_field).to_have_value(value)

    def click_login_button(self) -> None:
        self._login_button.click()

    def error_message_is_displayed(self) -> None:
        expect(self._error_message).to_be_visible()

    def check_negative_message_text(self, expected_mgs: str) -> None:
        expect(self._error_message).to_have_text(expected_mgs)


