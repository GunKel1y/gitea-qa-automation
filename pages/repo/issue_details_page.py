import os
import re

from playwright.sync_api import Page, expect

from pages.repo.base_repo_page import BaseRepoPage


class IssueDetailsPage(BaseRepoPage):

    def __init__(self, page: Page):
        super().__init__(page)
        self._issue_title = page.locator("div.issue-title>h1")
        self._issue_id = page.locator("div.issue-title>h1>span.index")
        self._issue_status_label = page.locator("div.issue-state-label")
        self._first_timeline_comment = page.locator(
            "div.timeline-item.first>div.comment-container>div.comment-body>div.render-content.markup"
        )
        self._switch_status_button = page.locator("button#status-button")
        self._switch_status_button_test = page.locator("button#status-button>span.status-button-text")
        self._update_title_button = page.locator("button#issue-title-edit-show")
        self._update_title_field = page.locator("form#issue-title-editor>div>input[name='title']")
        self._save_new_title_button = page.locator("div.issue-title-buttons>button[type='submit']")

        self._first_comment_container = page.locator("div.timeline-item.first")
        self._first_comment_context_dropdown = self._first_comment_container.locator("div.context-dropdown")
        self._edit_button_in_first_comment_dropdown_menu = self._first_comment_container.locator(
            "div.menu div.edit-content"
        )
        self._edit_comment_field_in_first_comment = self._first_comment_container.locator(
            "div[role='article'] div[data-tab-panel='markdown-writer'] textarea.markdown-text-editor"
        )
        self._save_new_comment_button = self._first_comment_container.locator(
            "div.flex-text-block>button[type='submit']"
        )

    def open(self, *, repo_owner: str, repo_name: str, issue_index: int) -> None:
        self.page.goto(f"{os.getenv("BASE_URL_UI")}/{repo_owner}/{repo_name}/issues/{issue_index}")

    def get_issue_id(self) -> str:
        return self._issue_id.inner_text()

    def issue_title_is_displayed(self) -> None:
        expect(self._issue_title).to_be_visible()

    def check_issue_title_value(self, expected_title_with_id: str) -> None:
        expect(self._issue_title).to_have_text(expected_title_with_id)

    def check_issue_status_label_text(self, status_text: str) -> None:
        expect(self._issue_status_label).to_have_text(status_text)

    def check_first_comment_text(self, comment_text: str) -> None:
        expect(self._first_timeline_comment).to_have_text(comment_text)

    def switch_status_button_click(self) -> None:
        self._switch_status_button.click()

    def check_switch_status_button_text(self, value: str) -> None:
        expect(self._switch_status_button).to_have_text(value)

    def click_update_title_button(self):
        self._update_title_button.click()

    def fill_update_title_field(self, new_issue_title: str):
        self._update_title_field.fill(new_issue_title)

    def click_save_new_title_button(self):
        self._save_new_title_button.click()

    def click_first_comment_context_dropdown(self) -> None:
        self._first_comment_context_dropdown.click()

    def click_edit_button_in_first_comment_dropdown_menu(self) -> None:
        self._edit_button_in_first_comment_dropdown_menu.click()
        expect(self._edit_comment_field_in_first_comment).to_be_visible()
        expect(self._edit_comment_field_in_first_comment).not_to_have_value("")

    def fill_edit_comment_field_in_first_comment(self, new_comment_text: str) -> None:
        self._edit_comment_field_in_first_comment.fill(new_comment_text)

    def click_save_new_comment_button(self) -> None:
        self._save_new_comment_button.click()