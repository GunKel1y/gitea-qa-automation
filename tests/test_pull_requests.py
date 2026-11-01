import allure
import pytest
from playwright.sync_api import Page

from pages.repo.compare_changes_page import CompareChangesPage
from pages.repo.pull_request_files_page import PullRequestFilesPage
from pages.repo.pull_request_page import PullRequestPage
from pages.repo.repo_pull_requests_page import RepoPullRequestsPage


pytestmark = allure.epic("Запросы на слияние")

BASE_BRANCH = "main"


@allure.testcase("TC-P-001")
@allure.title("Создание PR из ветки с изменениями")
@allure.severity(allure.severity_level.BLOCKER)
@pytest.mark.p0
def test_create_pr_from_branch_with_changes(
    authenticated_user_page: Page, created_initialized_public_repo, created_branch_with_commit, test_user
):
    repo_prs_page = RepoPullRequestsPage(authenticated_user_page)
    compare_changes_page = CompareChangesPage(authenticated_user_page)
    pr_page = PullRequestPage(authenticated_user_page)
    pr_files_page = PullRequestFilesPage(authenticated_user_page)
    owner_repo = test_user["login"]
    repo_name = created_initialized_public_repo["repo_name"]
    new_branch_name = created_branch_with_commit["branch_name"]
    code_diff = created_branch_with_commit["content"]
    pr_title = "Добавить " + created_branch_with_commit["file_name"]

    with allure.step("Открыть страницу создания запроса на слияние"):
        repo_prs_page.open(repo_owner=owner_repo, repo_name=repo_name)
        repo_prs_page.click_new_pr_button()
        compare_changes_page.check_url(f"/{owner_repo}/{repo_name}/compare/{BASE_BRANCH}...{BASE_BRANCH}")

    with allure.step('Выбрать ветку с изменениями в выпадающем списке "Взять из:"'):
        compare_changes_page.click_take_from_branch_dropdown()
        compare_changes_page.select_dropdown_item(new_branch_name)
        compare_changes_page.check_url(f"/{owner_repo}/{repo_name}/compare/{BASE_BRANCH}...{new_branch_name}")

    with allure.step("Проверить изменения по коммитам, файлам и коду"):
        compare_changes_page.check_count_commit(1)
        compare_changes_page.check_branches_in_commits_header(base_branch=BASE_BRANCH, take_from_branch=new_branch_name)
        compare_changes_page.pr_diff.check_diff_code_value(code_diff)

    with allure.step("Создать запрос на слияние"):
        compare_changes_page.click_new_pr_button()
        compare_changes_page.check_default_pr_title_field(pr_title)
        compare_changes_page.click_comment_create_pr_button()

    pr_id = pr_page.get_pr_id()
    pr_id_without_number_sign = pr_id.replace("#", "")

    with allure.step("Проверить заголовок и статус запроса на слияние"):
        pr_page.check_url(f"/{owner_repo}/{repo_name}/pulls/{pr_id_without_number_sign}")
        pr_page.check_pr_status_label_text("Открыто")
        pr_page.check_pr_title_value(expected_title=pr_title, expected_id=pr_id)

    with allure.step('Открыть вкладку "Изменённые файлы" и проверить изменения'):
        pr_page.open_diff_files_tab()
        pr_files_page.pr_diff.check_diff_code_value(code_diff)
