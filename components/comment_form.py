from playwright.sync_api import Locator, expect


class CommentForm:

    def __init__(self, comment: Locator):
        self.comment = comment
        self._body = comment.locator("div.comment-container div.comment-body div.render-content.markup")
        self._context_dropdown = comment.locator("div.context-dropdown")
        self._edit_item = comment.locator("div.menu div.edit-content")
        self._delete_item = comment.locator("div.menu div.delete-comment")
        self._input = comment.locator(
            "div[data-tab-panel='markdown-writer'] textarea.markdown-text-editor"
        )
        self._edit_save_button = comment.locator("div.flex-text-block>button[type='submit']")
        self._comment_button = comment.locator("button#comment-button")

    def check_text(self, comment_text: str) -> None:
        expect(self._body).to_have_text(comment_text)

    def click_context_dropdown(self) -> None:
        self._context_dropdown.click()

    def click_edit_item_in_menu(self) -> None:
        self._edit_item.click()
        expect(self._input).to_be_visible()
        expect(self._input).not_to_have_value("")

    def click_delete_item_in_menu(self, *, confirm: bool) -> None:
        def action(dialog):
            dialog.accept() if confirm else dialog.dismiss()

        self.comment.page.once("dialog", action)
        self._delete_item.click()

    def fill_input(self, new_comment: str) -> None:
        self._input.fill(new_comment)

    def click_edit_save_button(self) -> None:
        self._edit_save_button.click()

    def click_comment_button(self) -> None:
        self._comment_button.click()

    def check_visible(self) -> None:
        expect(self.comment).to_be_visible()

    def check_absence(self) -> None:
        expect(self.comment).not_to_be_visible()