import os

import pytest
from playwright.sync_api import Page

from helpers.test_data import repo_name_with_length, random_repo_name

from pages.create_repository_page import CreateRepositoryPage
from pages.dashboard_page import DashboardPage
from pages.not_found_error_page import NotFoundErrorPage
from pages.repo_page import RepoPage

@pytest.mark.parametrize("case",
                         ["min", "max", "greater_max", "with_space", "with_slash", "unicode_with_emoji", "default_name"]
                         )
def test_name_validation(authenticated_user_page: Page, test_user, case):
    dashboard_page = DashboardPage(authenticated_user_page)
    create_repo_page = CreateRepositoryPage(authenticated_user_page)
    repo_page = RepoPage(authenticated_user_page)

    dashboard_page.open()
    dashboard_page.global_header.create_dropdown_button_is_displayed()

    dashboard_page.global_header.click_dropdown_button()
    dashboard_page.global_header.create_new_repository_button_is_displayed()

    dashboard_page.global_header.click_create_new_repository_button()
    create_repo_page.check_url(f"{os.getenv("BASE_URL_UI")}/repo/create")
    create_repo_page.create_repo_form_is_displayed()
    create_repo_page.repo_name_field_is_displayed()

    if case == "min":
        repo_name = "a"
        create_repo_page.fill_repo_name_field("a")
        create_repo_page.check_repo_name_field_value("a")
    elif case == "greater_max":
        repo_name = repo_name_with_length(100)
        create_repo_page.fill_repo_name_field(repo_name + "T")
        create_repo_page.check_repo_name_field_value(repo_name)
    elif case == "max":
        repo_name = repo_name_with_length(100)
        create_repo_page.fill_repo_name_field(repo_name)
        create_repo_page.check_repo_name_field_value(repo_name)
    elif case == "with_slash":
        repo_name = repo_name_with_length(1) + "/" + repo_name_with_length(1)
        create_repo_page.fill_repo_name_field(repo_name)
        create_repo_page.check_repo_name_field_value(repo_name)
        repo_name = repo_name.replace("/", "-")
    elif case == "with_space":
        repo_name = repo_name_with_length(1) + " " + repo_name_with_length(1)
        create_repo_page.fill_repo_name_field(repo_name)
        create_repo_page.check_repo_name_field_value(repo_name)
        repo_name = repo_name.replace(" ", "-")
    elif case == "unicode_with_emoji":
        repo_name = "test-⭐"
        create_repo_page.fill_repo_name_field(repo_name)
        create_repo_page.check_repo_name_field_value(repo_name)
        repo_name = repo_name.replace("⭐", f"-")
    else:
        repo_name = random_repo_name()
        create_repo_page.fill_repo_name_field(repo_name)
        create_repo_page.check_repo_name_field_value(repo_name)

    create_repo_page.click_repo_create_button()
    repo_page.check_url(f"{os.getenv("BASE_URL_UI")}/{test_user['login']}/{repo_name}")
    repo_page.repo_name_in_header_is_displayed(username=test_user["login"], repo_name=repo_name)
    repo_page.empty_repo_guide_is_displayed()

@pytest.mark.parametrize("case", ["empty_name", "with_double_dot", "emoji", "duplicate_repo"])
def test_name_validation_no_repo_create(authenticated_user_page: Page, created_public_repo, case):
    dashboard_page = DashboardPage(authenticated_user_page)
    create_repo_page = CreateRepositoryPage(authenticated_user_page)

    dashboard_page.open()
    dashboard_page.global_header.click_dropdown_button()
    dashboard_page.global_header.click_create_new_repository_button()
    create_repo_page.check_url(f"{os.getenv('BASE_URL_UI')}/repo/create")
    if case == "with_double_dot":
        repo_name = ".."
        create_repo_page.fill_repo_name_field(repo_name)
        create_repo_page.check_repo_name_field_value(repo_name)
    elif case == "emoji":
        repo_name = "⭐"
        create_repo_page.fill_repo_name_field(repo_name)
        create_repo_page.check_repo_name_field_value(repo_name)
    elif case == "duplicate_repo":
        create_repo_page.fill_repo_name_field(created_public_repo["repo_name"])
        create_repo_page.check_repo_name_field_value(created_public_repo["repo_name"])

    create_repo_page.click_repo_create_button()

    if case == "duplicate_repo":
        create_repo_page.error_message_is_displayed()
        create_repo_page.check_negative_message_text("Название репозитория уже используется.")

    create_repo_page.check_url(f"{os.getenv('BASE_URL_UI')}/repo/create")
    create_repo_page.create_repo_form_is_displayed()

@pytest.mark.parametrize("case", ["public", "private"])
def test_create_repo(authenticated_user_page: Page, created_public_repo, test_user, case):
    create_repo_page = CreateRepositoryPage(authenticated_user_page)
    repo_page = RepoPage(authenticated_user_page)
    repo_name = random_repo_name()

    create_repo_page.open()

    create_repo_page.fill_repo_name_field(repo_name)
    create_repo_page.check_repo_name_field_value(repo_name)

    if case == "private":
        create_repo_page.select_checkbox_private_repo()
        create_repo_page.verify_activated_checkbox_private_repo()

    create_repo_page.click_repo_create_button()
    repo_page.repo_name_in_header_is_displayed(repo_name=repo_name, username=test_user["login"])
    repo_page.check_url(f'{os.getenv("BASE_URL_UI")}/{test_user["login"]}/{repo_name}')

    if case == "private":
        repo_page.privacy_status_is_displayed()

def test_check_private_repo_is_inaccessible_to_another_user(
        authenticated_second_user_page: Page, created_private_repo, test_user
):
    repo_page = RepoPage(authenticated_second_user_page)
    not_found_page = NotFoundErrorPage(authenticated_second_user_page)
    repo_page.open(username=test_user['login'], repo_name=created_private_repo['repo_name'])

    not_found_page.not_found_title_is_displayed()
    not_found_page.not_found_description_is_displayed()
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
    create_repo_page.check_repo_name_field_value(repo_name)

    create_repo_page.select_checkbox_initialization_repo()
    create_repo_page.verify_checkbox_activated_initialization_repo()

    create_repo_page.click_repo_create_button()
    repo_page.check_url(f"{os.getenv("BASE_URL_UI")}/{test_user["login"]}/{repo_name}")
    repo_page.repo_name_in_header_is_displayed(username=test_user["login"], repo_name=repo_name)

    repo_page.specified_file_in_list("README.md")
    repo_page.readme_content_is_displayed()

def test_create_repo_with_gitignore_and_readme_file(authenticated_user_page: Page, test_user):
    create_repo_page = CreateRepositoryPage(authenticated_user_page)
    repo_page = RepoPage(authenticated_user_page)
    repo_name = random_repo_name()

    create_repo_page.open()
    create_repo_page.fill_repo_name_field(repo_name)
    create_repo_page.check_repo_name_field_value(repo_name)

    create_repo_page.gitignore_dropdown.open()
    create_repo_page.gitignore_dropdown.menu_is_displayed()

    create_repo_page.gitignore_dropdown.select("Python")
    create_repo_page.gitignore_dropdown.tag_is_displayed("Python")

    create_repo_page.select_checkbox_initialization_repo()
    create_repo_page.verify_checkbox_activated_initialization_repo()

    create_repo_page.click_repo_create_button()
    repo_page.check_url(f"{os.getenv("BASE_URL_UI")}/{test_user["login"]}/{repo_name}")
    repo_page.repo_name_in_header_is_displayed(username=test_user["login"], repo_name=repo_name)
    repo_page.specified_file_in_list(".gitignore")
    repo_page.specified_file_in_list("README.md")

    repo_page.readme_content_is_displayed()

