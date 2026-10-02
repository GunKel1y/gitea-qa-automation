from playwright.sync_api import Page, Locator, expect


class IssueMetadata:

    def __init__(self, *, page: Page, metadata_name: str):
        self.page = page
        self.metadata_name = metadata_name
        self._metadata_container = page.locator(f"//div[contains(@data-update-url, '/issues/{metadata_name}')]")
        self._dropdown = self._metadata_container.locator(f"//div[contains(@class, 'dropdown')]")

    def _item_in_list_metadata(self, item_name: str) -> Locator:
        return self._metadata_container.locator(
            f"//div[contains(@class, 'list')]/a[.//text()[normalize-space(.)='{item_name}']]"
        )

    def _item_in_dropdown_menu(self, item_name: str) -> Locator:
        return self._metadata_container.locator(
            f"//div[contains(@class, 'scrolling menu')]"
            f"/a[contains(@class, 'item') and .//text()[normalize-space(.)='{item_name}']]"
        )

    def open(self) -> None:
        self._dropdown.click()

    def select_item(self, item_name: str) -> None:
        self._item_in_dropdown_menu(item_name).click()

    def check_item_in_list(self, item_name: str) -> None:
        expect(self._item_in_list_metadata(item_name)).to_be_visible()

    def check_item_absence_in_list(self, item_name: str) -> None:
        expect(self._item_in_list_metadata(item_name)).not_to_be_visible()

    def close(self) -> None:
        self.page.click("body")