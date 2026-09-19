import os

from pages.base_page import BasePage
from playwright.sync_api import Page, expect

class DashboardPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.__DASHBOARD = page.locator("div.dashboard[role='main']")
        self.__SUCCESS_REGISTRATION_BANNER  = page.locator('div.positive.message')
        self.__PROFILE_MENU_BUTTON = page.locator("div[data-tooltip-content='Профиль и настройки...']")
        self.__PROFILE_MENU = page.locator("div.menu[id='_aria_dropdown_menu_5']")
        self.__MENU_EXIT_BUTTON = page.locator("a[href='/user/logout']")

    def open(self):
        self.page.goto(os.getenv("BASE_URL_UI"))

    def dashboard_is_displayed(self) -> None:
        expect(self.__DASHBOARD).to_be_visible()

    def success_registration_banner_is_displayed(self) -> None:
        expect(self.__SUCCESS_REGISTRATION_BANNER).to_be_visible()

    def check_success_registration_banner_text(self, expected: str):
        expect(self.__SUCCESS_REGISTRATION_BANNER).to_have_text(expected)

    def check_url(self, expected: str) -> None:
        expect(self.page).to_have_url(expected)

    def click_profile_menu_button(self):
        self.__PROFILE_MENU_BUTTON.click()

    def profile_menu_button_is_displayed(self):
        expect(self.__PROFILE_MENU_BUTTON).to_be_visible()

    def profile_menu_is_displayed(self):
        expect(self.__PROFILE_MENU).to_be_visible()

    def menu_exit_button_is_displayed(self):
        expect(self.__MENU_EXIT_BUTTON).to_be_visible()

    def click_menu_exit_button(self):
        self.__MENU_EXIT_BUTTON.click()