from playwright.sync_api import Page, expect

from helpers.allure_helpers import step


class PullRequestsDiff:
    def __init__(self, page: Page):
        super().__init__(page)
        self._diff_file_container = page.locator("div.diff-file-box")
        self._diff_code = self._diff_file_container.locator("tr.add-code code.code-inner")


    @step('Проверить изменения в файле. Ожидается значение: "{code}"')
    def check_diff_code_value(self, code: str) -> None:
        expect(self._diff_code).to_have_text(code)
