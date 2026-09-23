from pages.base_page import BasePage
from playwright.sync_api import Page, expect


class NotFoundErrorPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self._error_title = page.locator("div[role='main']>div>div.status-page-error>div.status-page-error-title")
        self._error_description = page.locator(
            "div[role='main']>div>div.status-page-error>div.tw-text-center>div.tw-my-4"
        )

    def not_found_title_is_displayed(self) -> None:
        expect(self._error_title).to_be_visible()

    def not_found_description_is_displayed(self) -> None:
        expect(self._error_description).to_be_visible()

    def check_title_text(self, text: str) -> None:
        expect(self._error_title).to_have_text(text)

    def check_description_text(self, text: str) -> None:
        expect(self._error_description).to_have_text(text)

