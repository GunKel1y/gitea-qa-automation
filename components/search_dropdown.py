from playwright.sync_api import Page, Locator, expect


class SearchDropdown:

    def __init__(self, page: Page, field_name: str):
        self.page = page
        self.field_name = field_name
        self._input = page.locator(f"*[name='{field_name}']~input.search")
        self._menu = page.locator(f"input[name='{field_name}']~div.menu")
        self._tags = page.locator(f"input[name='{field_name}']~a")

    def _item(self, value: str) -> Locator:
        return self._menu.locator(f"div[data-value='{value}']")

    def open(self) -> None:
        self._input.click()

    def menu_is_displayed(self) -> None:
        expect(self._menu).to_be_visible()

    def select(self, value: str) -> None:
        self._item(value).click()

    def tag_is_displayed(self, value: str) -> None:
        expect(self.page.locator(f"input[name='{self.field_name}']~a[data-value='{value}']")).to_be_visible()