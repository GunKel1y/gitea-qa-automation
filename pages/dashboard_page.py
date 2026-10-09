import os

from pages.base_page import BasePage
from playwright.sync_api import Page, expect

class DashboardPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self._dashboard = page.locator("div.dashboard[role='main']")
        self._success_registration_banner  = page.locator('div.positive.message')
        self._switch_user_button = page.locator("div.secondary div.dropdown[role='menu']>span")
        self._switch_user_image = self._switch_user_button.locator("img")

    def open(self) -> None:
        self.page.goto(os.getenv("GITEA_UI_URL"))

    def dashboard_is_displayed(self) -> None:
        expect(self._dashboard).to_be_visible()

    def check_success_registration_banner_text(self, expected: str) -> None:
        expect(self._success_registration_banner).to_have_text(expected)

    def switch_user_button_is_displayed(self) -> None:
        expect(self._switch_user_button).to_be_visible()

    def switch_user_image_is_displayed(self) -> None:
        expect(self._switch_user_image).to_be_visible()