import os

from pages.base_page import BasePage
from playwright.sync_api import Page, expect

class RepoPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.__EMPTY_REPO_GUIDE = page.locator("div.content>div.empty-repo-guide")

    def open(self, *, username: str, repo_name: str):
        self.page.goto(f"{os.getenv("BASE_URL_UI")}/{username}/{repo_name}")

    def empty_repo_guide_is_displayed(self):
        expect(self.__EMPTY_REPO_GUIDE).to_be_visible()