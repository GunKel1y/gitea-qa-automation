from pages.base_page import BasePage
from playwright.sync_api import Page, expect


class NotFoundErrorPage(BasePage):

    DESCRIPTION = "Либо страница, которую вы пытаетесь открыть, не существует, либо у вас недостаточно прав для ее просмотра."

    def __init__(self, page: Page):
        super().__init__(page)
        self._error_title = page.locator(".status-page-error-title")
        self._error_block = page.locator(".status-page-error")

    def check_title_text(self) -> None:
        expect(self._error_title).to_have_text("404 Not Found")

    def check_description_text(self) -> None:
        expect(self._error_block).to_contain_text(self.DESCRIPTION)