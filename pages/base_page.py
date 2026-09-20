
from playwright.sync_api import Page, expect


class BasePage:

    def __init__(self, page: Page):
        self.page = page

    def check_url(self, expected: str) -> None:
        expect(self.page).to_have_url(expected)