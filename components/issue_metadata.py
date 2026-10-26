from playwright.sync_api import Locator, Page, expect

from helpers.allure_helpers import step


class IssueMetadata:
    def __init__(self, *, page: Page, container: Locator, name: str):
        self.page = page
        self.name = name
        self._metadata_container = container
        self._dropdown = container.locator("xpath=.//div[contains(@class, 'dropdown')]")

    def _item_in_list_metadata(self, item_name: str) -> Locator:
        return self._metadata_container.locator(
            f"//div[contains(@class, 'list')]/a[.//text()[normalize-space(.)='{item_name}']]"
        )

    def _item_in_dropdown_menu(self, item_name: str) -> Locator:
        return self._metadata_container.locator(
            f"//div[contains(@class, 'scrolling menu')]"
            f"/a[contains(@class, 'item') and .//text()[normalize-space(.)='{item_name}']]"
        )

    @step("Открыть список «{self.name}»")
    def open(self) -> None:
        self._dropdown.click()

    @step("Выбрать {item_name} в списке «{self.name}»")
    def select_item(self, item_name: str) -> None:
        self._item_in_dropdown_menu(item_name).click()

    @step("Проверить, что {item_name} есть в списке «{self.name}»")
    def check_item_in_list(self, item_name: str) -> None:
        expect(self._item_in_list_metadata(item_name)).to_be_visible()

    @step("Проверить, что {item_name} нет в списке «{self.name}»")
    def check_item_absence_in_list(self, item_name: str) -> None:
        expect(self._item_in_list_metadata(item_name)).not_to_be_visible()

    @step("Закрыть список «{self.name}»")
    def close(self) -> None:
        self.page.click("body")
