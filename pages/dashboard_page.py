
from pages.base_page import BasePage
from playwright.sync_api import Page, expect

class DashboardPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.__DASHBOARD = page.locator("div.dashboard[role='main']")

    def dashboard_is_displayed(self):
        expect(self.__DASHBOARD).to_be_visible()