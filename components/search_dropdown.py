import random

from playwright.sync_api import Page, Locator, expect


class SearchDropdown:

    def __init__(self, page: Page, field_name: str):
        self.page = page
        self.field_name = field_name
        self._input = page.locator(f"*[name='{field_name}']~input.search")
        self._menu = page.locator(f"input[name='{field_name}']~div.menu")
        self._item_list = self._menu.locator("div.item[data-value]:not([data-value=''])")
        self._tags = page.locator(f"input[name='{field_name}']~a")
        self._text_in_input = page.locator(f"*[name='{field_name}']~input.search~div.text")

    def _item(self, value: str) -> Locator:
        return self._menu.locator(f"div[data-value='{value}']")

    def _get_random_item(self) -> str:
        expect(
            self._item_list,
            "Невозможно выбрать рандомный элемент, так как не отображается список"
        ).not_to_have_count(0)
        return random.choice(self._item_list.all()).get_attribute("data-value")

    def open(self) -> None:
        self._input.click()

    def select(self, value: str) -> None:
        self._item(value).click()

    def select_random_item(self) -> None:
        self._item(self._get_random_item()).click()