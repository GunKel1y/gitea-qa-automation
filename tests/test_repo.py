import pytest
from playwright.sync_api import Page

from helpers.test_data import unique_name, value_with_length

from pages.repo.create_repository_page import CreateRepositoryPage
from pages.dashboard_page import DashboardPage
from pages.not_found_error_page import NotFoundErrorPage
from pages.repo.repo_issues_page import RepoIssuesPage
from pages.repo.repo_page import RepoPage

@pytest.mark.parametrize("repo_name, expected_name", [
    pytest.param("a", "a", id="min", marks=pytest.mark.p3),
    pytest.param("a" * 100, "a" * 100, id="max", marks=pytest.mark.p3),
    pytest.param("a" * 101, "a" * 100, id="over_max_truncated", marks=pytest.mark.p3),
    pytest.param("a b", "a-b", id="with_space", marks=pytest.mark.p3),
    pytest.param("a/b", "a-b", id="with_slash", marks=pytest.mark.p3),
    pytest.param("test-⭐", "test--", id="emoji", marks=pytest.mark.p2),
])
def test_name_validation(authenticated_user_page: Page, test_user, repo_name, expected_name):
    create_repo_page = CreateRepositoryPage(authenticated_user_page)
    repo_page = RepoPage(authenticated_user_page)

    create_repo_page.open()
    create_repo_page.fill_repo_name_field(repo_name)
    create_repo_page.click_repo_create_button()
    repo_page.check_url(f"/{test_user['login']}/{expected_name}")
    repo_page.repo_header.repo_name_in_header_is_displayed(username=test_user["login"], repo_name=expected_name)
    repo_page.empty_repo_guide_is_displayed()

@pytest.mark.parametrize("input_name", [
    pytest.param("", id="empty_name", marks=pytest.mark.p2),
    pytest.param("..", id="with_double_dot", marks=pytest.mark.p2),
    pytest.param("⭐", id="emoji", marks=pytest.mark.p2)
])
def test_name_validation_no_repo_create(authenticated_user_page: Page, input_name):
    create_repo_page = CreateRepositoryPage(authenticated_user_page)

    create_repo_page.open()
    create_repo_page.check_url("/repo/create")

    create_repo_page.fill_repo_name_field(input_name)

    create_repo_page.click_repo_create_button()

    create_repo_page.check_url("/repo/create")
    create_repo_page.create_repo_form_is_displayed()

@pytest.mark.p2
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

@pytest.mark.p0
def test_create_public_repo(authenticated_user_page: Page, test_user):
    create_repo_page = CreateRepositoryPage(authenticated_user_page)
    repo_page = RepoPage(authenticated_user_page)
    repo_name = unique_name(prefix='repo')

    create_repo_page.open()

    create_repo_page.fill_repo_name_field(repo_name)

    create_repo_page.click_repo_create_button()
    repo_page.repo_header.repo_name_in_header_is_displayed(repo_name=repo_name, username=test_user["login"])
    repo_page.check_url(f'/{test_user["login"]}/{repo_name}')

@pytest.mark.p1
def test_create_private_repo(authenticated_user_page: Page, test_user):
    create_repo_page = CreateRepositoryPage(authenticated_user_page)
    repo_page = RepoPage(authenticated_user_page)
    repo_name = unique_name(prefix='repo')

    create_repo_page.open()

    create_repo_page.fill_repo_name_field(repo_name)

    create_repo_page.select_checkbox_private_repo()

    create_repo_page.click_repo_create_button()
    repo_page.repo_header.repo_name_in_header_is_displayed(repo_name=repo_name, username=test_user["login"])
    repo_page.check_url(f'/{test_user["login"]}/{repo_name}')

    repo_page.privacy_status_is_displayed()

@pytest.mark.p3
def test_create_repo_by_template(authenticated_user_page: Page, test_user, created_template_repo):
    create_repo_page = CreateRepositoryPage(authenticated_user_page)
    repo_page = RepoPage(authenticated_user_page)
    repo_name = unique_name(prefix='repo')
    template_repo_name = created_template_repo["repo_name"]
    username = test_user["login"]

    create_repo_page.open()

    create_repo_page.fill_repo_name_field(repo_name)
    create_repo_page.repo_template.open()
    create_repo_page.repo_template.select(created_template_repo["repo_id"])
    create_repo_page.select_checkbox_git_content()
    create_repo_page.click_repo_create_button()

    repo_page.check_url(f'/{username}/{repo_name}')
    repo_page.repo_header.repo_name_in_header_is_displayed(repo_name=repo_name, username=username)
    repo_page.specified_file_in_list(".gitignore")
    repo_page.specified_file_in_list("LICENSE")
    repo_page.specified_file_in_list("README.md")
    repo_page.check_readme_title(template_repo_name)
    repo_page.check_readme_text(created_template_repo["description"])
    repo_page.repo_header.check_created_by_repo_text(owner_template=username, repo_template=template_repo_name)

@pytest.mark.p3
@pytest.mark.parametrize("labels_template, label_item", [
       pytest.param("Advanced", "Kind/Bug", id="advanced_labels"),
       pytest.param("Default", "help wanted", id="default_labels")
   ])
def test_create_repo_with_label_template(authenticated_user_page: Page, test_user, labels_template, label_item):
    create_repo_page = CreateRepositoryPage(authenticated_user_page)
    repo_issues_page = RepoIssuesPage(authenticated_user_page)

    username = test_user["login"]
    repo_name = unique_name(prefix='repo')

    create_repo_page.open()
    create_repo_page.fill_repo_name_field(repo_name)
    create_repo_page.issue_labels.open()
    create_repo_page.issue_labels.select(labels_template)
    create_repo_page.click_repo_create_button()

    repo_issues_page.open(username=username, repo_name=repo_name)
    repo_issues_page.open_labels_dropdown()
    repo_issues_page.labels_item_should_be_visible(label_item)

@pytest.mark.p1
def test_private_repo_is_inaccessible_to_another_user(
        authenticated_second_user_page: Page, created_private_repo, test_user
):
    repo_page = RepoPage(authenticated_second_user_page)
    not_found_page = NotFoundErrorPage(authenticated_second_user_page)
    repo_page.open(username=test_user['login'], repo_name=created_private_repo['repo_name'])

    not_found_page.check_title_text()
    not_found_page.check_description_text()

@pytest.mark.p1
def test_create_repo_with_readme_file(authenticated_user_page: Page, test_user):
    create_repo_page = CreateRepositoryPage(authenticated_user_page)
    repo_page = RepoPage(authenticated_user_page)
    repo_name = unique_name(prefix='user')

    create_repo_page.open()
    create_repo_page.fill_repo_name_field(repo_name)

    create_repo_page.select_checkbox_initialization_repo()

    create_repo_page.click_repo_create_button()
    repo_page.check_url(f"/{test_user["login"]}/{repo_name}")
    repo_page.repo_header.repo_name_in_header_is_displayed(username=test_user["login"], repo_name=repo_name)

    repo_page.specified_file_in_list("README.md")
    repo_page.readme_content_is_displayed()

@pytest.mark.p1
def test_create_repo_with_gitignore_and_readme_file(authenticated_user_page: Page, test_user):
    create_repo_page = CreateRepositoryPage(authenticated_user_page)
    repo_page = RepoPage(authenticated_user_page)
    repo_name = unique_name(prefix='repo')

    create_repo_page.open()
    create_repo_page.fill_repo_name_field(repo_name)

    create_repo_page.gitignore_dropdown.open()
    create_repo_page.gitignore_dropdown.select_random_item()

    create_repo_page.select_checkbox_initialization_repo()

    create_repo_page.click_repo_create_button()
    repo_page.check_url(f"/{test_user["login"]}/{repo_name}")
    repo_page.repo_header.repo_name_in_header_is_displayed(username=test_user["login"], repo_name=repo_name)
    repo_page.specified_file_in_list(".gitignore")
    repo_page.specified_file_in_list("README.md")

    repo_page.readme_content_is_displayed()

@pytest.mark.p1
def test_create_repo_with_license_and_readme_file(authenticated_user_page: Page, test_user):
    create_repo_page = CreateRepositoryPage(authenticated_user_page)
    repo_page = RepoPage(authenticated_user_page)
    repo_name = unique_name(prefix='repo')

    create_repo_page.open()
    create_repo_page.fill_repo_name_field(repo_name)

    create_repo_page.license_dropdown.open()
    create_repo_page.license_dropdown.select_random_item()

    create_repo_page.select_checkbox_initialization_repo()

    create_repo_page.click_repo_create_button()
    repo_page.check_url(f"/{test_user["login"]}/{repo_name}")
    repo_page.repo_header.repo_name_in_header_is_displayed(username=test_user["login"], repo_name=repo_name)
    repo_page.specified_file_in_list("LICENSE")
    repo_page.specified_file_in_list("README.md")
    repo_page.readme_content_is_displayed()

@pytest.mark.p1
def test_create_repo_with_license_readme_and_gitignore_files(authenticated_user_page: Page, test_user):
    create_repo_page = CreateRepositoryPage(authenticated_user_page)
    repo_page = RepoPage(authenticated_user_page)
    repo_name = unique_name(prefix='repo')

    create_repo_page.open()
    create_repo_page.fill_repo_name_field(repo_name)

    create_repo_page.gitignore_dropdown.open()
    create_repo_page.gitignore_dropdown.select_random_item()
    create_repo_page.press_esc()

    create_repo_page.license_dropdown.open()
    create_repo_page.license_dropdown.select_random_item()

    create_repo_page.select_checkbox_initialization_repo()

    create_repo_page.click_repo_create_button()
    repo_page.check_url(f"/{test_user["login"]}/{repo_name}")
    repo_page.repo_header.repo_name_in_header_is_displayed(username=test_user["login"], repo_name=repo_name)
    repo_page.specified_file_in_list("LICENSE")
    repo_page.specified_file_in_list(".gitignore")
    repo_page.specified_file_in_list("README.md")
    repo_page.readme_content_is_displayed()

@pytest.mark.parametrize("input_branch, expected_branch", [
    pytest.param("tests-master", "tests-master", id="custom_branch", marks=pytest.mark.p1),
    pytest.param("", "main", id="empty_field_in_default_branch_field", marks=pytest.mark.p3)
])
def test_create_repo_default_branch(authenticated_user_page: Page, test_user, input_branch, expected_branch):
    create_repo_page = CreateRepositoryPage(authenticated_user_page)
    repo_page = RepoPage(authenticated_user_page)
    repo_name = unique_name(prefix='repo')

    create_repo_page.open()
    create_repo_page.fill_repo_name_field(repo_name)

    create_repo_page.select_checkbox_initialization_repo()

    create_repo_page.fill_default_branch_field(input_branch)

    create_repo_page.click_repo_create_button()
    repo_page.check_url(f"/{test_user["login"]}/{repo_name}")
    repo_page.repo_header.repo_name_in_header_is_displayed(username=test_user["login"], repo_name=repo_name)
    repo_page.branch_dropdown_button_is_displayed()
    repo_page.check_branch_dropdown_button_text(expected_branch)
    repo_page.specified_file_in_list("README.md")
    repo_page.readme_content_is_displayed()

@pytest.mark.p1
def test_create_repo_in_organization(authenticated_user_page: Page, created_public_organization_by_user):
    create_repo_page = CreateRepositoryPage(authenticated_user_page)
    repo_page = RepoPage(authenticated_user_page)
    repo_name = unique_name(prefix='repo')
    org_name = created_public_organization_by_user["name"]

    create_repo_page.open()

    create_repo_page.owner_field_click()
    create_repo_page.select_owner(org_name)

    create_repo_page.fill_repo_name_field(repo_name)
    create_repo_page.click_repo_create_button()

    repo_page.check_url(f"/{org_name}/{repo_name}")
    repo_page.repo_header.repo_name_in_header_is_displayed(username=org_name, repo_name=repo_name)

@pytest.mark.p2
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

@pytest.mark.p1
def test_public_repo_is_accessible_to_another_user(
        authenticated_second_user_page: Page, created_public_repo, test_user
):
    repo_page = RepoPage(authenticated_second_user_page)
    user_login = test_user['login']
    repo_name = created_public_repo['repo_name']
    repo_page.open(username=user_login, repo_name=repo_name)

    repo_page.repo_header.repo_name_in_header_is_displayed(repo_name=repo_name, username=user_login)
    repo_page.check_url(f'/{test_user["login"]}/{repo_name}')

@pytest.mark.p2
def test_create_repo_with_description(authenticated_user_page: Page, test_user):
    create_repo_page = CreateRepositoryPage(authenticated_user_page)
    repo_page = RepoPage(authenticated_user_page)
    repo_name = unique_name(prefix="repo")
    repo_description = unique_name(prefix="description")

    create_repo_page.open()

    create_repo_page.fill_repo_name_field(repo_name)
    create_repo_page.fill_repo_description(repo_description)
    create_repo_page.select_checkbox_initialization_repo()

    create_repo_page.click_repo_create_button()
    repo_page.repo_header.repo_name_in_header_is_displayed(repo_name=repo_name, username=test_user["login"])
    repo_page.check_repo_description_text(repo_description)
    repo_page.check_url(f'/{test_user["login"]}/{repo_name}')

@pytest.mark.p3
def test_trying_create_repo_with_exceeding_description_value(authenticated_user_page: Page, test_user):
    create_repo_page = CreateRepositoryPage(authenticated_user_page)
    repo_page = RepoPage(authenticated_user_page)
    repo_name = unique_name(prefix="repo")
    description = value_with_length(3000)

    create_repo_page.open()

    create_repo_page.fill_repo_name_field(repo_name)
    create_repo_page.fill_repo_description(description)
    create_repo_page.repo_description_value_should_be_equal(description[:2048])
    create_repo_page.select_checkbox_initialization_repo()
    create_repo_page.click_repo_create_button()

    repo_page.check_url(f"/{test_user["login"]}/{repo_name}")
    repo_page.check_repo_description_text(description[:2048])


@pytest.mark.p3
def test_create_repo_with_value_exceeding_maximum_for_default_branch(authenticated_user_page: Page):
    create_repo_page = CreateRepositoryPage(authenticated_user_page)
    repo_name = unique_name(prefix="repo")
    default_branch = value_with_length(101)

    create_repo_page.open()

    create_repo_page.fill_repo_name_field(repo_name)
    create_repo_page.fill_default_branch_field(default_branch)
    create_repo_page.select_checkbox_initialization_repo()
    create_repo_page.click_repo_create_button()

    create_repo_page.check_url("/repo/create")
    create_repo_page.error_message_has_text("form.DefaultBranch должен содержать максимум 100 символов.")

@pytest.mark.p3
def test_create_repo_with_default_branch_upper_limit_value(authenticated_user_page: Page, test_user):
    create_repo_page = CreateRepositoryPage(authenticated_user_page)
    repo_page = RepoPage(authenticated_user_page)
    repo_name = unique_name(prefix="repo")
    default_branch = value_with_length(100)

    create_repo_page.open()

    create_repo_page.fill_repo_name_field(repo_name)
    create_repo_page.fill_default_branch_field(default_branch)
    create_repo_page.select_checkbox_initialization_repo()
    create_repo_page.click_repo_create_button()

    repo_page.check_url(f"/{test_user["login"]}/{repo_name}")
    repo_page.check_branch_dropdown_button_text(default_branch)
