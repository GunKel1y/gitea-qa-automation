import os
import re

from playwright.sync_api import Page, expect, Locator

from components.comment_form import CommentForm
from components.issue_metadata import IssueMetadata
from pages.repo.base_repo_page import BaseRepoPage


class IssueDetailsPage(BaseRepoPage):

    def __init__(self, page: Page):
        super().__init__(page)
        self._issue_title = page.locator("div.issue-title>h1")
        self._issue_id = page.locator("div.issue-title>h1>span.index")
        self._issue_status_label = page.locator("div.issue-state-label")
        self._switch_status_button = page.locator("button#status-button")
        self._switch_status_button_test = page.locator("button#status-button>span.status-button-text")
        self._update_title_button = page.locator("button#issue-title-edit-show")
        self._update_title_field = page.locator("form#issue-title-editor>div>input[name='title']")
        self._save_new_title_button = page.locator("div.issue-title-buttons>button[type='submit']")
        self.labels = IssueMetadata(page=page, container=self._by_update_url("labels"))
        self.assignees = IssueMetadata(page=page, container=self._by_update_url("assignee"))
        self.milestones = IssueMetadata(page=page, container=self._by_update_url("milestone"))

    def _by_update_url(self, name: str) -> Locator:
        return self.page.locator(f"//div[contains(@data-update-url, '/issues/{name}')]")

    def first_comment(self) -> CommentForm:
        return CommentForm(self.page.locator("div.timeline-item.comment.first"))

    def comment_by_id(self, comment_id: int) -> CommentForm:
        return CommentForm(self.page.locator(f"#issuecomment-{comment_id}"))

    def comment_by_text(self, comment_text: str) -> CommentForm:
        return CommentForm(self.page.locator("div.timeline-item.comment:not(.form)").filter(has_text=comment_text))

    def open(self, *, repo_owner: str, repo_name: str, issue_index: int) -> None:
        self.page.goto(f"{os.getenv("GITEA_UI_URL")}/{repo_owner}/{repo_name}/issues/{issue_index}")

    def get_issue_id(self) -> str:
        return self._issue_id.inner_text()

    def issue_title_is_displayed(self) -> None:
        expect(self._issue_title).to_be_visible()

    def check_issue_title_value(self, *, expected_title: str, expected_id: str) -> None:
        full_expected_text = f"{expected_title} {expected_id}"
        expect(self._issue_title).to_have_text(full_expected_text)

    def check_issue_status_label_text(self, status_text: str) -> None:
        expect(self._issue_status_label).to_have_text(status_text)

    def switch_status_button_click(self) -> None:
        self._switch_status_button.click()

    def check_switch_status_button_text(self, value: str) -> None:
        expect(self._switch_status_button).to_have_text(value)

    def switch_status_button_should_be_hidden(self) -> None:
        expect(self._switch_status_button).to_be_hidden()

    def update_title_button_should_be_hidden(self) -> None:
        expect(self._update_title_button).to_be_hidden()

    def click_update_title_button(self):
        self._update_title_button.click()

    def fill_update_title_field(self, new_issue_title: str):
        self._update_title_field.fill(new_issue_title)

    def click_save_new_title_button(self):
        self._save_new_title_button.click()

    def new_comment_form(self) -> CommentForm:
        return CommentForm(self.page.locator("div.timeline-item.comment.form"))