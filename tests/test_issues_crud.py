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
    issue_page.check_first_comment_text(comment_text)