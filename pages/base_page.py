import os

from playwright.sync_api import Page, expect

from components.global_header import GlobalHeader
from helpers.allure_helpers import step


class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.global_header = GlobalHeader(page)
        self._error_message = page.locator("div.negative.message.flash-message.flash-error")
        self._invalid_fields = page.locator(":invalid")

    @step("Проверить, что URL страницы {expected_endpoint}")
    def check_url(self, expected_endpoint: str) -> None:
        expect(self.page).to_have_url(f"{os.getenv('GITEA_UI_URL')}{expected_endpoint}")

    @step("Проверить, что текст ошибки {text}")
    def error_message_has_text(self, text: str) -> None:
        expect(self._error_message).to_have_text(text)

    @step("Открыть настройки пользователя")
    def open_user_settings(self) -> None:
        self.page.goto(f"{os.getenv('GITEA_UI_URL')}/user/settings")

    @step("Открыть профиль пользователя {login}")
    def open_profile_user(self, login: str) -> None:
        self.page.goto(f"{os.getenv('GITEA_UI_URL')}/{login}")
