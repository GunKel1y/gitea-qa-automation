import os

from playwright.sync_api import Page, expect

from components.global_header import GlobalHeader


class BasePage:

    def __init__(self, page: Page):
        self.page = page
        self.global_header = GlobalHeader(page)

    def check_url(self, expected_endpoint: str) -> None:
        expect(self.page).to_have_url(f"{os.getenv("BASE_URL_UI")}{expected_endpoint}")