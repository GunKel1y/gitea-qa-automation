import pytest

from playwright.sync_api import Page

from helpers.test_data import random_login
from pages.repo.issue_details_page import IssueDetailsPage
from pages.repo.new_issues_page import NewIssuesPage
from pages.repo.repo_issues_page import RepoIssuesPage


def test_add_issue_with_minimal_data(authenticated_user_page: Page, created_public_repo, test_user):
    repo_issues_page = RepoIssuesPage(authenticated_user_page)
    new_issues_page = NewIssuesPage(authenticated_user_page)
    issue_page = IssueDetailsPage(authenticated_user_page)
    issue_name = random_login()

    repo_issues_page.open(username=test_user["login"], repo_name=created_public_repo["repo_name"])
    repo_issues_page.click_new_issues_button()

    new_issues_page.fill_input_issue_title(issue_name)
    new_issues_page.click_add_issue_button()

    issue_page.issue_title_is_displayed()
    issue_page.check_issue_status_label_text("Открыто")

    issue_id = issue_page.get_issue_id()
    issue_page.check_issue_title_value(issue_name + " " + issue_id)

def test_add_issue_with_comment(authenticated_user_page: Page, created_public_repo, test_user):
    repo_issues_page = RepoIssuesPage(authenticated_user_page)
    new_issues_page = NewIssuesPage(authenticated_user_page)
    issue_page = IssueDetailsPage(authenticated_user_page)
    issue_name = random_login()
    comment_text = random_login()

    repo_issues_page.open(username=test_user["login"], repo_name=created_public_repo["repo_name"])
    repo_issues_page.click_new_issues_button()

    new_issues_page.fill_input_issue_title(issue_name)
    new_issues_page.fill_comment(comment_text)
    new_issues_page.click_add_issue_button()

    issue_page.issue_title_is_displayed()
    issue_page.check_issue_status_label_text("Открыто")

    issue_id = issue_page.get_issue_id()
    issue_page.check_issue_title_value(issue_name + " " + issue_id)
    issue_page.first_comment().check_text(comment_text)

@pytest.mark.parametrize("issue_status, switch_button_text", [
    pytest.param("Закрыто", "Открыть снова", id="closing"),
    pytest.param("Открыто", "Закрыть задачу", id="reopen")
]
)
def test_switch_issue_status(
        authenticated_user_page,
        test_user,
        created_public_repo,
        created_repo_issue,
        issue_status,
        switch_button_text
):
    issue_page = IssueDetailsPage(authenticated_user_page)

    issue_page.open(
        repo_owner=test_user["login"],
        repo_name=created_public_repo["repo_name"],
        issue_index=created_repo_issue["issue_index"]
    )

    issue_page.switch_status_button_click()
    issue_page.check_issue_status_label_text(issue_status)
    issue_page.check_switch_status_button_text(switch_button_text)

def test_update_issue_title(authenticated_user_page: Page, created_public_repo, created_repo_issue, test_user):
    issue_page = IssueDetailsPage(authenticated_user_page)
    new_issue_title = random_login()

    issue_page.open(
        repo_owner=test_user["login"],
        repo_name=created_public_repo["repo_name"],
        issue_index=created_repo_issue["issue_index"]
    )

    issue_page.click_update_title_button()
    issue_page.fill_update_title_field(new_issue_title)
    issue_page.click_save_new_title_button()
    issue_page.check_issue_title_value(new_issue_title + " #" + str(created_repo_issue["issue_index"]))

def test_update_issue_comment(authenticated_user_page: Page, created_public_repo, created_repo_issue, test_user):
    issue_page = IssueDetailsPage(authenticated_user_page)
    new_issue_comment = random_login()

    issue_page.open(
        repo_owner=test_user["login"],
        repo_name=created_public_repo["repo_name"],
        issue_index=created_repo_issue["issue_index"]
    )

    issue_page.first_comment().click_context_dropdown()
    issue_page.first_comment().click_edit_item_in_menu()
    issue_page.first_comment().fill_edit_input(new_issue_comment)
    issue_page.first_comment().click_edit_save_button()

    issue_page.first_comment().check_text(new_issue_comment)

def test_adding_issue_label(
        authenticated_user_page: Page,
        created_public_repo,
        created_repo_issue,
        created_label_on_issue,
        test_user):
    issue_page = IssueDetailsPage(authenticated_user_page)
    issue_label_text = created_label_on_issue["label_name"]

    issue_page.open(
        repo_owner=test_user["login"],
        repo_name=created_public_repo["repo_name"],
        issue_index=created_repo_issue["issue_index"]
    )

    issue_page.click_labels_dropdown()
    issue_page.click_labels_item(issue_label_text)
    issue_page.click_on_empty_space()
    issue_page.check_tag_in_labels_list(issue_label_text)

def test_removing_label_from_issue(
        authenticated_user_page: Page,
        created_public_repo,
        created_repo_issue_with_label,
        test_user
):
    issue_page = IssueDetailsPage(authenticated_user_page)
    label_name = created_repo_issue_with_label["label_name"]

    issue_page.open(
        repo_owner=test_user["login"],
        repo_name=created_public_repo["repo_name"],
        issue_index=created_repo_issue_with_label["issue_index"]
    )

    issue_page.click_labels_dropdown()
    issue_page.click_labels_item(label_name)
    issue_page.click_on_empty_space()
    issue_page.check_tag_absence_in_labels_list(label_name)