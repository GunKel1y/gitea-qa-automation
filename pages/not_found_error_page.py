from playwright.sync_api import Page, expect

from helpers.allure_helpers import step
from pages.base_page import BasePage


class NotFoundErrorPage(BasePage):
    DESCRIPTION = (
        "Либо страница, которую вы пытаетесь открыть, не существует, либо у вас недостаточно прав для ее просмотра."
    )

    def __init__(self, page: Page):
        super().__init__(page)
        self._error_title = page.locator(".status-page-error-title")
        self._error_block = page.locator(".status-page-error")

    @step("Проверить заголовок страницы 404")
    def check_title_text(self) -> None:
        expect(self._error_title).to_have_text("404 Not Found")

    @step("Проверить описание страницы 404")
    def check_description_text(self) -> None:
        expect(self._error_block).to_contain_text(self.DESCRIPTION)
