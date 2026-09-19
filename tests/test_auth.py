import os

from playwright.sync_api import Page, expect
from pages.auth_page import AuthPage
from pages.dashboard_page import DashboardPage



def test_login_with_valid_creds(page: Page, register_person_for_auth):
    auth_page = AuthPage(page)
    dashboard_page = DashboardPage(page)

    person_login = register_person_for_auth[0]
    person_pass = register_person_for_auth[1]

    auth_page.auth_form_is_displayed()

    auth_page.fill_username(person_login)
    auth_page.check_value_username(person_login)
    auth_page.fill_password(person_pass)
    auth_page.check_value_password(person_pass)
    auth_page.click_register_account_button()

    auth_page.check_url(f'{os.getenv("BASE_URL_UI")}/')
    dashboard_page.dashboard_is_displayed()