import allure
import pytest

from playwright.sync_api import Page

from components.comment_form import CommentForm
from conftest import created_closed_repo_issue
from helpers.test_data import unique_name, value_with_length, MAX_TITLE_LENGTH
from pages.not_found_error_page import NotFoundErrorPage
from pages.repo.issue_details_page import IssueDetailsPage
from pages.repo.new_issues_page import NewIssuesPage
from pages.repo.repo_issues_page import RepoIssuesPage

@allure.testcase("TC-I-001")
@pytest.mark.p0
def test_add_issue_with_minimal_data(authenticated_user_page: Page, created_public_repo, test_user):
    repo_issues_page = RepoIssuesPage(authenticated_user_page)
    new_issues_page = NewIssuesPage(authenticated_user_page)
    issue_page = IssueDetailsPage(authenticated_user_page)
    issue_name = unique_name(prefix='issue')

    repo_issues_page.open(username=test_user["login"], repo_name=created_public_repo["repo_name"])
    repo_issues_page.click_new_issues_button()

    new_issues_page.fill_input_issue_title(issue_name)
    new_issues_page.click_add_issue_button()

    issue_id = issue_page.get_issue_id().replace("#", "")
    issue_page.check_url(f"/{test_user["login"]}/{created_public_repo["repo_name"]}/issues/{issue_id}")
    issue_page.issue_title_is_displayed()
    issue_page.check_issue_status_label_text("Открыто")

    issue_id = issue_page.get_issue_id()
    issue_page.check_issue_title_value(expected_title=issue_name, expected_id=issue_id)

@allure.testcase("TC-I-010")
@pytest.mark.p1
def test_add_issue_with_pinned_comment(authenticated_user_page: Page, created_public_repo, test_user):
    repo_issues_page = RepoIssuesPage(authenticated_user_page)
    new_issues_page = NewIssuesPage(authenticated_user_page)
    issue_page = IssueDetailsPage(authenticated_user_page)
    issue_name = unique_name(prefix='issue')
    comment_text = unique_name(prefix='comment')

    repo_issues_page.open(username=test_user["login"], repo_name=created_public_repo["repo_name"])
    repo_issues_page.click_new_issues_button()

    new_issues_page.fill_input_issue_title(issue_name)
    new_issues_page.fill_comment(comment_text)
    new_issues_page.click_add_issue_button()

    issue_id = issue_page.get_issue_id().replace("#", "")
    issue_page.check_url(f"/{test_user["login"]}/{created_public_repo["repo_name"]}/issues/{issue_id}")
    issue_page.issue_title_is_displayed()
    issue_page.check_issue_status_label_text("Открыто")

    issue_id = issue_page.get_issue_id()
    issue_page.check_issue_title_value(expected_title=issue_name, expected_id=issue_id)
    issue_page.first_comment().check_text(comment_text)

@pytest.mark.parametrize("issue_status, switch_button_text, fixture_name", [
    pytest.param("Закрыто", "Открыть снова", "created_repo_issue", id="closing", marks=[pytest.mark.p0, allure.testcase("TC-I-002")]),
    pytest.param("Открыто", "Закрыть задачу", "created_closed_repo_issue", id="reopen", marks=[pytest.mark.p1, allure.testcase("TC-I-011")])
])
def test_switch_issue_status(
        authenticated_user_page,
        test_user,
        created_public_repo,
        issue_status,
        switch_button_text,
        fixture_name,
        request
):
    issue_page = IssueDetailsPage(authenticated_user_page)
    issue_data = request.getfixturevalue(fixture_name)

    issue_page.open(
        repo_owner=test_user["login"],
        repo_name=created_public_repo["repo_name"],
        issue_index=issue_data["issue_index"]
    )

    issue_page.switch_status_button_click()
    issue_page.check_issue_status_label_text(issue_status)
    issue_page.check_switch_status_button_text(switch_button_text)

@allure.testcase("TC-I-012a")
@pytest.mark.p1
def test_update_issue_title(authenticated_user_page: Page, created_public_repo, created_repo_issue, test_user):
    issue_page = IssueDetailsPage(authenticated_user_page)
    new_issue_title = unique_name(prefix='issue')

    issue_page.open(
        repo_owner=test_user["login"],
        repo_name=created_public_repo["repo_name"],
        issue_index=created_repo_issue["issue_index"]
    )

    issue_page.click_update_title_button()
    issue_page.fill_update_title_field(new_issue_title)
    issue_page.click_save_new_title_button()
    issue_page.check_issue_title_value(
        expected_title=new_issue_title, expected_id=f"#{created_repo_issue['issue_index']}"
    )

@allure.testcase("TC-I-012b")
@pytest.mark.p1
def test_update_issue_pinned_comment(authenticated_user_page: Page, created_public_repo, created_repo_issue, test_user):
    issue_page = IssueDetailsPage(authenticated_user_page)
    new_issue_comment = unique_name(prefix='comment')

    issue_page.open(
        repo_owner=test_user["login"],
        repo_name=created_public_repo["repo_name"],
        issue_index=created_repo_issue["issue_index"]
    )

    issue_page.first_comment().click_context_dropdown()
    issue_page.first_comment().click_edit_item_in_menu()
    issue_page.first_comment().fill_input(new_issue_comment)
    issue_page.first_comment().click_edit_save_button()

    issue_page.first_comment().check_text(new_issue_comment)

@allure.testcase("TC-I-013")
@pytest.mark.p1
def test_adding_issue_label(
        authenticated_user_page: Page,
        created_public_repo,
        created_repo_issue,
        created_repo_label,
        test_user):
    issue_page = IssueDetailsPage(authenticated_user_page)
    issue_label_text = created_repo_label["label_name"]

    issue_page.open(
        repo_owner=test_user["login"],
        repo_name=created_public_repo["repo_name"],
        issue_index=created_repo_issue["issue_index"]
    )

    issue_page.labels.open()
    issue_page.labels.select_item(issue_label_text)
    issue_page.labels.close()
    issue_page.labels.check_item_in_list(issue_label_text)

@allure.testcase("TC-I-014")
@pytest.mark.p1
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

    issue_page.labels.open()
    issue_page.labels.select_item(label_name)
    issue_page.labels.close()
    issue_page.labels.check_item_absence_in_list(label_name)

@allure.testcase("TC-I-015")
@pytest.mark.p1
def test_adding_issue_assignee(
        authenticated_user_page: Page,
        created_public_repo,
        created_repo_issue,
        test_user
):
    issue_page = IssueDetailsPage(authenticated_user_page)

    issue_page.open(
        repo_owner=test_user["login"],
        repo_name=created_public_repo["repo_name"],
        issue_index=created_repo_issue["issue_index"]
    )

    issue_page.assignees.open()
    issue_page.assignees.select_item(test_user["login"])
    issue_page.assignees.close()
    issue_page.assignees.check_item_in_list(test_user["login"])

@allure.testcase("TC-I-016")
@pytest.mark.p1
def test_issue_linking_with_milestone(
        authenticated_user_page: Page,
        created_public_repo,
        created_repo_issue,
        created_milestone,
        test_user
):
    issue_page = IssueDetailsPage(authenticated_user_page)
    milestone_name = created_milestone["milestone_name"]

    issue_page.open(
        repo_owner=test_user["login"],
        repo_name=created_public_repo["repo_name"],
        issue_index=created_repo_issue["issue_index"]
    )

    issue_page.milestones.open()
    issue_page.milestones.select_item(milestone_name)
    issue_page.milestones.close()
    issue_page.milestones.check_item_in_list(milestone_name)

@allure.testcase("TC-I-017")
@pytest.mark.p1
def test_adding_timeline_comment(authenticated_user_page: Page, created_public_repo, created_repo_issue, test_user):
    issue_page = IssueDetailsPage(authenticated_user_page)
    comment_text = unique_name(prefix='comment')

    issue_page.open(
        repo_owner=test_user["login"],
        repo_name=created_public_repo["repo_name"],
        issue_index=created_repo_issue["issue_index"]
    )

    issue_page.new_comment_form().fill_input(comment_text)
    issue_page.new_comment_form().click_comment_button()
    issue_page.comment_by_text(comment_text).check_visible()

@allure.testcase("TC-I-018")
@pytest.mark.p1
def test_update_timeline_comment(
        authenticated_user_page: Page,
        created_public_repo,
        created_repo_issue,
        created_timeline_comment,
        test_user):
    issue_page = IssueDetailsPage(authenticated_user_page)
    update_comment_text = unique_name(prefix='comment')
    comment_id=created_timeline_comment["comment_id"]

    issue_page.open(
        repo_owner=test_user["login"],
        repo_name=created_public_repo["repo_name"],
        issue_index=created_repo_issue["issue_index"]
    )

    issue_page.comment_by_id(comment_id).click_context_dropdown()
    issue_page.comment_by_id(comment_id).click_edit_item_in_menu()
    issue_page.comment_by_id(comment_id).fill_input(update_comment_text)
    issue_page.comment_by_id(comment_id).click_edit_save_button()
    issue_page.comment_by_id(comment_id).check_text(update_comment_text)

@pytest.mark.parametrize("confirm, check_result", [
    pytest.param(True, CommentForm.check_absence,
                 id="confirm_delete", marks=[pytest.mark.p1, allure.testcase("TC-I-019")]
    ),
    pytest.param(False, CommentForm.check_visible,
                 id="cancel_delete", marks=[pytest.mark.p1, allure.testcase("TC-I-019b")]),
])
def test_delete_timeline_comment(
        authenticated_user_page: Page,
        created_public_repo,
        created_repo_issue,
        created_timeline_comment,
        test_user,
        confirm,
        check_result
):
    issue_page = IssueDetailsPage(authenticated_user_page)
    comment_id=created_timeline_comment["comment_id"]

    issue_page.open(
        repo_owner=test_user["login"],
        repo_name=created_public_repo["repo_name"],
        issue_index=created_repo_issue["issue_index"]
    )

    comment = issue_page.comment_by_id(comment_id)
    comment.click_context_dropdown()
    comment.click_delete_item_in_menu(confirm=confirm)
    check_result(comment)

@allure.testcase("TC-I-020")
@pytest.mark.p1
def test_adding_timeline_comment_with_closed_issue_status(
        authenticated_user_page: Page,
        created_public_repo,
        created_closed_repo_issue,
        test_user):
    issue_page = IssueDetailsPage(authenticated_user_page)
    comment_text = unique_name(prefix='comment')

    issue_page.open(
        repo_owner=test_user["login"],
        repo_name=created_public_repo["repo_name"],
        issue_index=created_closed_repo_issue["issue_index"]
    )

    issue_page.check_issue_status_label_text("Закрыто")

    issue_page.new_comment_form().fill_input(comment_text)
    issue_page.new_comment_form().click_comment_button()
    issue_page.comment_by_text(comment_text).check_visible()
    issue_page.comment_by_text(comment_text).check_text(comment_text)
    issue_page.check_issue_status_label_text("Закрыто")

@allure.testcase("TC-I-030")
@pytest.mark.p2
def test_add_issue_with_empty_title(
        authenticated_user_page: Page,
        created_public_repo,
        test_user):
    new_issue_page = NewIssuesPage(authenticated_user_page)
    repo_owner = test_user["login"]
    repo_name = created_public_repo["repo_name"]

    new_issue_page.open(repo_owner=repo_owner, repo_name=repo_name)
    new_issue_page.click_add_issue_button()

    new_issue_page.check_url(f"/{repo_owner}/{repo_name}/issues/new")
    new_issue_page.check_show_error_in_required_title()

@allure.testcase("TC-I-032")
@pytest.mark.p2
def test_add_issue_with_disabled_has_issue_param_in_repo(
        authenticated_user_page: Page,
        test_user,
        created_public_repo,
        disabling_ability_add_issue_to_repo):
    new_issue_page = NewIssuesPage(authenticated_user_page)
    not_found_page = NotFoundErrorPage(authenticated_user_page)
    repo_owner = test_user["login"]
    repo_name = created_public_repo["repo_name"]

    new_issue_page.open(repo_owner=repo_owner, repo_name=repo_name)

    not_found_page.check_url(f"/{repo_owner}/{repo_name}/issues/new")
    not_found_page.check_title_text()
    not_found_page.check_description_text()

@allure.testcase("TC-I-036")
@pytest.mark.p2
def test_creating_issue_with_label(
        authenticated_user_page: Page,
        test_user,
        created_public_repo,
        created_repo_label):
    new_issue_page = NewIssuesPage(authenticated_user_page)
    issue_page = IssueDetailsPage(authenticated_user_page)
    issue_name = unique_name(prefix='issue')
    label_item = created_repo_label["label_name"]

    new_issue_page.open(
        repo_owner=test_user["login"],
        repo_name=created_public_repo["repo_name"]
    )
    new_issue_page.fill_input_issue_title(issue_name)

    new_issue_page.labels.open()
    new_issue_page.labels.select_item(label_item)
    new_issue_page.labels.close()
    new_issue_page.click_add_issue_button()

    issue_id = issue_page.get_issue_id().replace("#", "")
    issue_page.check_url(f"/{test_user["login"]}/{created_public_repo["repo_name"]}/issues/{issue_id}")
    issue_page.labels.check_item_in_list(label_item)

@allure.testcase("TC-I-037")
@pytest.mark.p2
def test_creating_issue_with_assignee(
        authenticated_user_page: Page,
        test_user,
        created_public_repo,
        adding_collaboration_for_repo_with_admin_permission
):
    new_issue_page = NewIssuesPage(authenticated_user_page)
    issue_page = IssueDetailsPage(authenticated_user_page)
    issue_name = unique_name(prefix='issue')
    collaborator_name = adding_collaboration_for_repo_with_admin_permission["collaborator_login"]

    new_issue_page.open(
        repo_owner=test_user["login"],
        repo_name=created_public_repo["repo_name"]
    )
    new_issue_page.fill_input_issue_title(issue_name)

    new_issue_page.assignees.open()
    new_issue_page.assignees.select_item(collaborator_name)
    new_issue_page.assignees.close()
    new_issue_page.click_add_issue_button()

    issue_id = issue_page.get_issue_id().replace("#", "")
    issue_page.check_url(f"/{test_user["login"]}/{created_public_repo["repo_name"]}/issues/{issue_id}")
    issue_page.assignees.check_item_in_list(collaborator_name)

@allure.testcase("TC-I-038")
@pytest.mark.p2
def test_creating_issue_with_milestone(
        authenticated_user_page: Page, test_user, created_public_repo, created_milestone
):
    new_issue_page = NewIssuesPage(authenticated_user_page)
    issue_page = IssueDetailsPage(authenticated_user_page)
    issue_name = unique_name(prefix='issue')
    milestone_name = created_milestone["milestone_name"]

    new_issue_page.open(
        repo_owner=test_user["login"],
        repo_name=created_public_repo["repo_name"]
    )
    new_issue_page.fill_input_issue_title(issue_name)

    new_issue_page.milestones.open()
    new_issue_page.milestones.select_item(milestone_name)
    new_issue_page.milestones.close()
    new_issue_page.click_add_issue_button()

    issue_id = issue_page.get_issue_id().replace("#", "")
    issue_page.check_url(f"/{test_user["login"]}/{created_public_repo["repo_name"]}/issues/{issue_id}")
    issue_page.milestones.check_item_in_list(milestone_name)

@allure.testcase("TC-I-040")
@pytest.mark.p2
def test_trying_update_issue_title_and_pinned_comment_by_other_user(
        test_user,
        authenticated_second_user_page,
        second_test_user,
        created_public_repo,
        created_repo_issue
):
    issue_page = IssueDetailsPage(authenticated_second_user_page)
    pinned_comment = issue_page.comment_by_text(created_repo_issue["issue_comment"])

    issue_page.open(
        repo_owner=test_user["login"],
        repo_name=created_public_repo["repo_name"],
        issue_index=created_repo_issue["issue_index"]
    )

    issue_page.update_title_button_should_be_hidden()
    pinned_comment.click_context_dropdown()
    pinned_comment.edit_item_should_be_hidden()

@allure.testcase("TC-I-041")
@pytest.mark.p2
def test_trying_close_issue_by_other_user(
        test_user,
        authenticated_second_user_page,
        created_public_repo,
        created_repo_issue
):
    issue_page = IssueDetailsPage(authenticated_second_user_page)

    issue_page.open(
        repo_owner=test_user["login"],
        repo_name=created_public_repo["repo_name"],
        issue_index=created_repo_issue["issue_index"]
    )

    issue_page.switch_status_button_should_be_hidden()

@allure.testcase("TC-I-042")
@pytest.mark.p2
def test_trying_update_and_delete_comment_by_other_user(
        test_user,
        authenticated_second_user_page,
        created_public_repo,
        created_repo_issue,
        created_timeline_comment
):
    issue_page = IssueDetailsPage(authenticated_second_user_page)
    comment = issue_page.comment_by_text(created_timeline_comment["comment_name"])

    issue_page.open(
        repo_owner=test_user["login"],
        repo_name=created_public_repo["repo_name"],
        issue_index=created_repo_issue["issue_index"]
    )

    comment.click_context_dropdown()
    comment.edit_item_should_be_hidden()
    comment.delete_should_be_hidden()

@allure.testcase("TC-I-043")
@pytest.mark.p2
def test_adding_timeline_comment_in_repo_by_other_user(
        test_user,
        authenticated_second_user_page,
        second_test_user,
        created_public_repo,
        created_repo_issue
):
    issue_page = IssueDetailsPage(authenticated_second_user_page)
    user_name = second_test_user["login"]
    comment = unique_name(prefix="comment")
    issue_page.open(
        repo_owner=test_user["login"],
        repo_name=created_public_repo["repo_name"],
        issue_index=created_repo_issue["issue_index"]
    )

    issue_page.new_comment_form().fill_input(comment)
    issue_page.new_comment_form().click_comment_button()

    timeline_comment = issue_page.comment_by_text(comment)
    timeline_comment.check_author(user_name)
    timeline_comment.check_text(comment)

@allure.testcase("TC-I-033")
@pytest.mark.p3
def test_adding_issue_with_max_length_title(
        test_user,
        authenticated_user_page,
        created_public_repo
):
    new_issue_page = NewIssuesPage(authenticated_user_page)
    issue_page = IssueDetailsPage(authenticated_user_page)
    title = value_with_length(length=MAX_TITLE_LENGTH+1)

    new_issue_page.open(
        repo_owner=test_user["login"],
        repo_name=created_public_repo["repo_name"]
    )

    new_issue_page.fill_input_issue_title(title)
    new_issue_page.issue_title_should_be_equal(title[:MAX_TITLE_LENGTH])
    new_issue_page.click_add_issue_button()
    issue_id = issue_page.get_issue_id()
    issue_page.check_issue_title_value(expected_title=title[:MAX_TITLE_LENGTH], expected_id=issue_id)