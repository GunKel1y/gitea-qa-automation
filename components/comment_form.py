from playwright.sync_api import Locator, expect

from helpers.allure_helpers import step


class CommentForm:
    def __init__(self, comment: Locator):
        self.comment = comment
        self._body = comment.locator("div.comment-container div.comment-body div.render-content.markup")
        self._context_dropdown = comment.locator("div.context-dropdown")
        self._edit_item = comment.locator("div.menu div.edit-content")
        self._delete_item = comment.locator("div.menu div.delete-comment")
        self._input = comment.locator("div[data-tab-panel='markdown-writer'] textarea.markdown-text-editor")
        self._edit_save_button = comment.locator("div.flex-text-block>button[type='submit']")
        self._comment_button = comment.locator("button#comment-button")

    def _header(self, author_name: str) -> Locator:
        return self.comment.locator(f'a.muted[href="/{author_name}"]')

    @step("Проверить автора комментария: {author_name}")
    def check_author(self, author_name: str) -> None:
        expect(self._header(author_name)).to_have_text(author_name)

    @step("Проверить текст комментария: {comment_text}")
    def check_text(self, comment_text: str) -> None:
        expect(self._body).to_have_text(comment_text, timeout=15_000)

    @step("Открыть меню комментария")
    def click_context_dropdown(self) -> None:
        self._context_dropdown.click()

    @step("Проверить, что пункт «Редактировать» скрыт")
    def edit_item_should_be_hidden(self) -> None:
        expect(self._edit_item).to_be_hidden()

    @step("Нажать «Редактировать» в меню комментария")
    def click_edit_item_in_menu(self) -> None:
        """Открывает редактор комментария и ждёт, пока поле появится и заполнится текущим текстом"""
        self._edit_item.click()
        expect(self._input).to_be_visible()
        expect(self._input).not_to_have_value("")

    @step("Нажать «Удалить» в меню комментария (подтверждение: {confirm})")
    def click_delete_item_in_menu(self, *, confirm: bool) -> None:
        """Нажимает "Удалить" и отвечает на нативный confirm: confirm=True - принять, False - отклонить

        Обработчик ставится до клика, так как без него Playwright сам отклонит диалог
        """

        def action(dialog):
            dialog.accept() if confirm else dialog.dismiss()

        self.comment.page.once("dialog", action)
        self._delete_item.click()

    @step("Проверить, что пункт «Удалить» скрыт")
    def delete_should_be_hidden(self) -> None:
        expect(self._delete_item).to_be_hidden()

    @step("Ввести текст комментария: {new_comment}")
    def fill_input(self, new_comment: str) -> None:
        self._input.fill(new_comment)

    @step("Сохранить изменённый комментарий")
    def click_edit_save_button(self) -> None:
        self._edit_save_button.click()

    @step("Нажать «Комментировать»")
    def click_comment_button(self) -> None:
        self._comment_button.click()

    @step("Проверить, что комментарий отображается")
    def check_visible(self) -> None:
        expect(self.comment).to_be_visible()

    @step("Проверить, что комментарий не отображается")
    def check_absence(self) -> None:
        expect(self.comment).not_to_be_visible()
