
from playwright.sync_api import Page, expect

class GlobalHeader:

    def __init__(self, page: Page):
        self.page = page
        self.__LOGIN_BUTTON = page.locator("a[href='/user/login']")
        self.__REGISTRATION_BUTTON = page.locator("a[href='/user/sign_up']")
        self.__PROFILE_AND_SETTINGS_MENU_BUTTON = page.locator("div[data-tooltip-content='Профиль и настройки...']")
        self.__PROFILE_MENU = page.locator("div.menu[id='_aria_dropdown_menu_5']")
        self.__MENU_EXIT_BUTTON = page.locator("a[href='/user/logout']")
        self.__CREATE_DROPDOWN_BUTTON = page.locator("div[data-tooltip-content='Создать…']")
        self.__CREATE_NEW_REPOSITORY_BUTTON = page.locator("a.item[href='/repo/create']")

    def login_button_is_displayed(self):
        expect(self.__LOGIN_BUTTON).to_be_visible()

    def registration_button_is_displayed(self):
        expect(self.__REGISTRATION_BUTTON).to_be_visible()

    def click_profile_menu_button(self):
        self.__PROFILE_AND_SETTINGS_MENU_BUTTON.click()

    def profile_menu_button_is_displayed(self):
        expect(self.__PROFILE_AND_SETTINGS_MENU_BUTTON).to_be_visible()

    def profile_menu_is_displayed(self):
        expect(self.__PROFILE_MENU).to_be_visible()

    def menu_exit_button_is_displayed(self):
        expect(self.__MENU_EXIT_BUTTON).to_be_visible()

    def click_menu_exit_button(self):
        self.__MENU_EXIT_BUTTON.click()

    def create_dropdown_button_is_displayed(self):
        expect(self.__CREATE_DROPDOWN_BUTTON).to_be_visible()

    def click_dropdown_button(self):
        self.__CREATE_DROPDOWN_BUTTON.click()

    def create_new_repository_button_is_displayed(self):
        expect(self.__CREATE_NEW_REPOSITORY_BUTTON).to_be_visible()

    def click_create_new_repository_button(self):
        self.__CREATE_NEW_REPOSITORY_BUTTON.click()