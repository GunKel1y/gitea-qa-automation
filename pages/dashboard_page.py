import os

from playwright.sync_api import Page, expect

from helpers.allure_helpers import step
from pages.base_page import BasePage


class DashboardPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self._dashboard = page.locator("div.dashboard[role='main']")
        self._success_registration_banner = page.locator("div.positive.message")
        self._switch_user_button = page.locator("div.secondary div.dropdown[role='menu']>span")
        self._switch_user_image = self._switch_user_button.locator("img")

    @step("Открыть главную страницу")
    def open(self) -> None:
        self.page.goto(os.getenv("GITEA_UI_URL"))

    @step("Проверить, что отображается панель управления")
    def dashboard_is_displayed(self) -> None:
        expect(self._dashboard).to_be_visible()

    @step("Проверить текст баннера об успешной регистрации: {expected}")
    def check_success_registration_banner_text(self, expected: str) -> None:
        expect(self._success_registration_banner).to_have_text(expected)

    @step("Проверить, что отображается кнопка переключения пользователя")
    def switch_user_button_is_displayed(self) -> None:
        expect(self._switch_user_button).to_be_visible()

    @step("Проверить, что отображается аватар в кнопке переключения пользователя")
    def switch_user_image_is_displayed(self) -> None:
        expect(self._switch_user_image).to_be_visible()
