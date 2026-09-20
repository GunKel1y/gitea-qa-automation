import os

from playwright.sync_api import Page

from pages.create_repository_page import CreateRepositoryPage
from pages.dashboard_page import DashboardPage
from pages.repo_page import RepoPage


def test_create_repo_minimal(authenticated_user_page: Page, test_user):
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

    create_repo_page.fill_repo_name_field("a")
    create_repo_page.check_repo_name_field_value("a")

    create_repo_page.click_repo_create_button()
    repo_page.check_url(f"{os.getenv("BASE_URL_UI")}/{test_user['login']}/a")
    repo_page.empty_repo_guide_is_displayed()