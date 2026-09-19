
from pages.base_page import BasePage
from playwright.sync_api import Page, expect

class DashboardPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.__DASHBOARD = page.locator("div.dashboard[role='main']")
        self.__SUCCESS_REGISTRATION_BANNER  = page.locator('div.positive.message')

    def dashboard_is_displayed(self) -> None:
        expect(self.__DASHBOARD).to_be_visible()

    def success_registration_banner_is_displayed(self) -> None:
        expect(self.__SUCCESS_REGISTRATION_BANNER).to_be_visible()

    def check_success_registration_banner_text(self, expected: str):
        expect(self.__SUCCESS_REGISTRATION_BANNER).to_have_text(expected)

    def check_url(self, expected: str) -> None:
        expect(self.page).to_have_url(expected)