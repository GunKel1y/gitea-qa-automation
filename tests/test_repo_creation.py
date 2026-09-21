import os

import pytest
from playwright.sync_api import Page

from helpers.test_data import repo_name_with_length

from pages.create_repository_page import CreateRepositoryPage
from pages.dashboard_page import DashboardPage
from pages.repo_page import RepoPage

@pytest.mark.parametrize("case", ["min", "max", "greater_max", "with_space", "with_slash", "unicode_with_emoji"])
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
    else:
        repo_name = "test-⭐"
        create_repo_page.fill_repo_name_field(repo_name)
        create_repo_page.check_repo_name_field_value(repo_name)
        repo_name = repo_name.replace("⭐", f"-")

    create_repo_page.click_repo_create_button()
    repo_page.check_url(f"{os.getenv("BASE_URL_UI")}/{test_user['login']}/{repo_name}")
    repo_page.repo_name_in_header_is_displayed(username=test_user["login"], repo_name=repo_name)
    repo_page.empty_repo_guide_is_displayed()

@pytest.mark.parametrize("case", ["empty_name", "with_double_dot", "emoji"])
def test_name_validation_no_repo_create(authenticated_user_page: Page, case):
    dashboard_page = DashboardPage(authenticated_user_page)
    create_repo_page = CreateRepositoryPage(authenticated_user_page)

    dashboard_page.open()
    dashboard_page.global_header.click_dropdown_button()
    dashboard_page.global_header.click_create_new_repository_button()

    if case == "with_double_dot":
        repo_name = ".."
        create_repo_page.fill_repo_name_field(repo_name)
        create_repo_page.check_repo_name_field_value(repo_name)
    elif case == "emoji":
        repo_name = "⭐"
        create_repo_page.fill_repo_name_field(repo_name)
        create_repo_page.check_repo_name_field_value(repo_name)

    create_repo_page.check_url(f"{os.getenv('BASE_URL_UI')}/repo/create")
    create_repo_page.click_repo_create_button()

    create_repo_page.check_url(f"{os.getenv('BASE_URL_UI')}/repo/create")
    create_repo_page.create_repo_form_is_displayed()