
from pages.base_page import BasePage
from playwright.sync_api import Page, expect


class AuthPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.__AUTH_FORM = page.locator("//div[@class='ui attached segment']/form[@action='/user/login']/..")
        self.__USERNAME_FIELD = page.locator("input#user_name")
        self.__PASSWORD_FIELD = page.locator("input#password")
        self.__LOGIN_BUTTON = page.locator('button.ui.primary.button')

    def auth_form_is_displayed(self) -> None:
        expect(self.__AUTH_FORM).to_be_visible()

    def fill_username(self, value: str) -> None:
        self.__USERNAME_FIELD.fill(value)

    def check_value_username(self, value: str) -> None:
        expect(self.__USERNAME_FIELD).to_have_value(value)

    def fill_password(self, value: str) -> None:
        self.__PASSWORD_FIELD.fill(value)

    def check_value_password(self, value: str) -> None:
        expect(self.__PASSWORD_FIELD).to_have_value(value)

    def click_register_account_button(self) -> None:
        self.__LOGIN_BUTTON.click()

    def check_url(self, expected: str) -> None:
        expect(self.page).to_have_url(expected)

