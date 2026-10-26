from playwright.sync_api import Page, expect

from helpers.allure_helpers import step


class GlobalHeader:
    def __init__(self, page: Page):
        self.page = page
        self._login_button = page.locator("a[href='/user/login']")
        self._registration_button = page.locator("a[href='/user/sign_up']")
        self._profile_and_settings_menu_button = page.locator("div[data-tooltip-content='Профиль и настройки...']")
        self._menu_exit_button = page.locator("a[href='/user/logout']")
        self._create_dropdown_button = page.locator("div[data-tooltip-content='Создать…']")
        self._create_new_repository_button = page.locator("a.item[href='/repo/create']")

    @step("Проверить, что в шапке отображается кнопка входа")
    def login_button_is_displayed(self) -> None:
        expect(self._login_button).to_be_visible()

    @step("Проверить, что в шапке отображается кнопка регистрации")
    def registration_button_is_displayed(self) -> None:
        expect(self._registration_button).to_be_visible()

    @step("Проверить, что в шапке отображается меню профиля")
    def profile_menu_button_is_displayed(self) -> None:
        expect(self._profile_and_settings_menu_button).to_be_visible()

    @step("Открыть меню профиля")
    def click_profile_menu_button(self) -> None:
        self._profile_and_settings_menu_button.click()

    @step("Нажать «Выйти»")
    def click_menu_exit_button(self) -> None:
        self._menu_exit_button.click()

    @step("Открыть меню «Создать»")
    def click_dropdown_button(self) -> None:
        self._create_dropdown_button.click()

    @step("Нажать «Новый репозиторий»")
    def click_create_new_repository_button(self) -> None:
        self._create_new_repository_button.click()
