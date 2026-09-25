import pytest
from playwright.sync_api import Page

from helpers.test_data import random_repo_name

from pages.create_repository_page import CreateRepositoryPage
from pages.dashboard_page import DashboardPage
from pages.not_found_error_page import NotFoundErrorPage
from pages.repo_page import RepoPage

@pytest.mark.parametrize("repo_name, expected_name", [
    pytest.param("a", "a", id="min"),
    pytest.param("a" * 100, "a" * 100, id="max"),
    pytest.param("a" * 101, "a" * 100, id="over_max_truncated"),
    pytest.param("a b", "a-b", id="with_space"),
    pytest.param("a/b", "a-b", id="with_slash"),
    pytest.param("test-⭐", "test--", id="emoji"),
])
def test_name_validation(authenticated_user_page: Page, test_user, repo_name, expected_name):
    create_repo_page = CreateRepositoryPage(authenticated_user_page)
    repo_page = RepoPage(authenticated_user_page)

    create_repo_page.open()
    create_repo_page.fill_repo_name_field(repo_name)
    create_repo_page.click_repo_create_button()
    repo_page.check_url(f"/{test_user['login']}/{expected_name}")
    repo_page.repo_name_in_header_is_displayed(username=test_user["login"], repo_name=expected_name)
    repo_page.empty_repo_guide_is_displayed()

@pytest.mark.parametrize("input_name", [
    pytest.param("", id="empty_name"),
    pytest.param("..", id="with_double_dot"),
    pytest.param("⭐", id="emoji")
])
def test_name_validation_no_repo_create(authenticated_user_page: Page, input_name):
    create_repo_page = CreateRepositoryPage(authenticated_user_page)

    create_repo_page.open()
    create_repo_page.check_url("/repo/create")

    create_repo_page.fill_repo_name_field(input_name)

    create_repo_page.click_repo_create_button()

    create_repo_page.check_url("/repo/create")
    create_repo_page.create_repo_form_is_displayed()

def test_create_repo_with_duplicate_name(authenticated_user_page: Page, created_public_repo):
    dashboard_page = DashboardPage(authenticated_user_page)
    create_repo_page = CreateRepositoryPage(authenticated_user_page)

    dashboard_page.open()
    dashboard_page.global_header.click_dropdown_button()
    dashboard_page.global_header.click_create_new_repository_button()
    create_repo_page.check_url("/repo/create")

    create_repo_page.fill_repo_name_field(created_public_repo["repo_name"])

    create_repo_page.click_repo_create_button()

    create_repo_page.error_message_has_text("Название репозитория уже используется.")

def test_create_public_repo(authenticated_user_page: Page, test_user):
    create_repo_page = CreateRepositoryPage(authenticated_user_page)
    repo_page = RepoPage(authenticated_user_page)
    repo_name = random_repo_name()

    create_repo_page.open()

    create_repo_page.fill_repo_name_field(repo_name)

    create_repo_page.click_repo_create_button()
    repo_page.repo_name_in_header_is_displayed(repo_name=repo_name, username=test_user["login"])
    repo_page.check_url(f'/{test_user["login"]}/{repo_name}')

def test_create_private_repo(authenticated_user_page: Page, test_user):
    create_repo_page = CreateRepositoryPage(authenticated_user_page)
    repo_page = RepoPage(authenticated_user_page)
    repo_name = random_repo_name()

    create_repo_page.open()

    create_repo_page.fill_repo_name_field(repo_name)

    create_repo_page.select_checkbox_private_repo()

    create_repo_page.click_repo_create_button()
    repo_page.repo_name_in_header_is_displayed(repo_name=repo_name, username=test_user["login"])
    repo_page.check_url(f'/{test_user["login"]}/{repo_name}')

    repo_page.privacy_status_is_displayed()

def test_private_repo_is_inaccessible_to_another_user(
        authenticated_second_user_page: Page, created_private_repo, test_user
):
    repo_page = RepoPage(authenticated_second_user_page)
    not_found_page = NotFoundErrorPage(authenticated_second_user_page)
    repo_page.open(username=test_user['login'], repo_name=created_private_repo['repo_name'])

    not_found_page.check_title_text("404 Not Found")
    not_found_page.check_description_text(
        "Либо страница, которую вы пытаетесь открыть, не существует, либо у вас недостаточно прав для ее просмотра."
    )

def test_create_repo_with_readme_file(authenticated_user_page: Page, test_user):
    create_repo_page = CreateRepositoryPage(authenticated_user_page)
    repo_page = RepoPage(authenticated_user_page)
    repo_name = random_repo_name()

    create_repo_page.open()
    create_repo_page.fill_repo_name_field(repo_name)

    create_repo_page.select_checkbox_initialization_repo()

    create_repo_page.click_repo_create_button()
    repo_page.check_url(f"/{test_user["login"]}/{repo_name}")
    repo_page.repo_name_in_header_is_displayed(username=test_user["login"], repo_name=repo_name)

    repo_page.specified_file_in_list("README.md")
    repo_page.readme_content_is_displayed()

def test_create_repo_with_gitignore_and_readme_file(authenticated_user_page: Page, test_user):
    create_repo_page = CreateRepositoryPage(authenticated_user_page)
    repo_page = RepoPage(authenticated_user_page)
    repo_name = random_repo_name()

    create_repo_page.open()
    create_repo_page.fill_repo_name_field(repo_name)

    create_repo_page.gitignore_dropdown.open()

    create_repo_page.gitignore_dropdown.select("Python")

    create_repo_page.select_checkbox_initialization_repo()

    create_repo_page.click_repo_create_button()
    repo_page.check_url(f"/{test_user["login"]}/{repo_name}")
    repo_page.repo_name_in_header_is_displayed(username=test_user["login"], repo_name=repo_name)
    repo_page.specified_file_in_list(".gitignore")
    repo_page.specified_file_in_list("README.md")

    repo_page.readme_content_is_displayed()

def test_create_repo_with_license_and_readme_file(authenticated_user_page: Page, test_user):
    create_repo_page = CreateRepositoryPage(authenticated_user_page)
    repo_page = RepoPage(authenticated_user_page)
    repo_name = random_repo_name()

    create_repo_page.open()
    create_repo_page.fill_repo_name_field(repo_name)

    create_repo_page.license_dropdown.open()

    create_repo_page.license_dropdown.select("Apache-2.0")

    create_repo_page.select_checkbox_initialization_repo()

    create_repo_page.click_repo_create_button()
    repo_page.check_url(f"/{test_user["login"]}/{repo_name}")
    repo_page.repo_name_in_header_is_displayed(username=test_user["login"], repo_name=repo_name)
    repo_page.specified_file_in_list("LICENSE")
    repo_page.specified_file_in_list("README.md")
    repo_page.readme_content_is_displayed()

def test_create_repo_with_license_readme_and_gitignore_files(authenticated_user_page: Page, test_user):
    create_repo_page = CreateRepositoryPage(authenticated_user_page)
    repo_page = RepoPage(authenticated_user_page)
    repo_name = random_repo_name()

    create_repo_page.open()
    create_repo_page.fill_repo_name_field(repo_name)

    create_repo_page.gitignore_dropdown.open()
    create_repo_page.gitignore_dropdown.select("Go")
    create_repo_page.press_esc()

    create_repo_page.license_dropdown.open()
    create_repo_page.license_dropdown.select("EPL-1.0")

    create_repo_page.select_checkbox_initialization_repo()

    create_repo_page.click_repo_create_button()
    repo_page.check_url(f"/{test_user["login"]}/{repo_name}")
    repo_page.repo_name_in_header_is_displayed(username=test_user["login"], repo_name=repo_name)
    repo_page.specified_file_in_list("LICENSE")
    repo_page.specified_file_in_list(".gitignore")
    repo_page.specified_file_in_list("README.md")
    repo_page.readme_content_is_displayed()

@pytest.mark.parametrize("input_branch, expected_branch",
    [
        pytest.param("tests-master", "tests-master", id="custom_branch"),
        pytest.param("", "main", id="empty_field_in_default_branch_field"),
    ]
)
def test_create_repo_default_branch(authenticated_user_page: Page, test_user, input_branch, expected_branch):
    create_repo_page = CreateRepositoryPage(authenticated_user_page)
    repo_page = RepoPage(authenticated_user_page)
    repo_name = random_repo_name()

    create_repo_page.open()
    create_repo_page.fill_repo_name_field(repo_name)

    create_repo_page.select_checkbox_initialization_repo()

    create_repo_page.fill_default_branch_field(input_branch)

    create_repo_page.click_repo_create_button()
    repo_page.check_url(f"/{test_user["login"]}/{repo_name}")
    repo_page.repo_name_in_header_is_displayed(username=test_user["login"], repo_name=repo_name)
    repo_page.branch_dropdown_button_is_displayed()
    repo_page.check_branch_dropdown_button_text(expected_branch)
    repo_page.specified_file_in_list("README.md")
    repo_page.readme_content_is_displayed()

def test_create_repo_in_organization(authenticated_user_page: Page, created_public_organization_by_user):
    create_repo_page = CreateRepositoryPage(authenticated_user_page)
    repo_page = RepoPage(authenticated_user_page)
    repo_name = random_repo_name()
    org_name = created_public_organization_by_user["name"]

    create_repo_page.open()

    create_repo_page.owner_field_click()
    create_repo_page.select_owner(org_name)

    create_repo_page.fill_repo_name_field(repo_name)
    create_repo_page.click_repo_create_button()

    repo_page.check_url(f"/{org_name}/{repo_name}")
    repo_page.repo_name_in_header_is_displayed(username=org_name, repo_name=repo_name)

def test_repo_create_without_creation_rights(
        authenticated_user_page: Page,
        created_organization_without_creation_rights,
        test_user
):
    create_repo_page = CreateRepositoryPage(authenticated_user_page)
    org_name = created_organization_without_creation_rights["name"]

    create_repo_page.open()

    create_repo_page.owner_field_click()
    create_repo_page.owner_is_selectable(test_user["login"])
    create_repo_page.owner_is_not_selectable(org_name)