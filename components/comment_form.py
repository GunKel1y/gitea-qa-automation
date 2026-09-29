from playwright.sync_api import Locator, expect


class CommentForm:

    def __init__(self, comment: Locator):
        self.comment = comment
        self._body = comment.locator("div.comment-container div.comment-body div.render-content.markup")
        self._context_dropdown = comment.locator("div.context-dropdown")
        self._edit_item = comment.locator("div.menu div.edit-content")
        self._edit_input = comment.locator(
            "div[data-tab-panel='markdown-writer'] textarea.markdown-text-editor"
        )
        self._edit_save_button = comment.locator("div.flex-text-block>button[type='submit']")

    def check_text(self, comment_text: str) -> None:
        expect(self._body).to_have_text(comment_text)

    def click_context_dropdown(self) -> None:
        self._context_dropdown.click()

    def click_edit_item_in_menu(self) -> None:
        self._edit_item.click()
        expect(self._edit_input).to_be_visible()
        expect(self._edit_input).not_to_have_value("")

    def fill_edit_input(self, new_comment: str) -> None:
        self._edit_input.fill(new_comment)

    def click_edit_save_button(self) -> None:
        self._edit_save_button.click()