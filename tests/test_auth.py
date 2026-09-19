import os

import pytest

from playwright.sync_api import Page, expect
from pages.auth_page import AuthPage
from pages.dashboard_page import DashboardPage

from helpers.test_data import random_password, random_login

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
    auth_page.click_login_button()

    auth_page.check_url(f'{os.getenv("BASE_URL_UI")}/')
    dashboard_page.dashboard_is_displayed()

@pytest.mark.parametrize("case", ["invalid_password", "non_exit_creds", "no_creds"])
def test_login_with_invalid_creds(page: Page, register_person_for_auth, case):
    auth_page = AuthPage(page)

    if case == "invalid_password":
        person_login, person_password = register_person_for_auth[0], register_person_for_auth[1] + "invalid"
    else:
        person_login, person_password = random_login(), random_password()

    auth_page.auth_form_is_displayed()

    auth_page.fill_username(person_login)
    auth_page.check_value_username(person_login)

    auth_page.fill_password(person_password)
    auth_page.check_value_password(person_password)

    auth_page.click_login_button()

    if case != "no_creds":
        auth_page.error_message_is_displayed()
        auth_page.check_negative_message_text('Неверное имя пользователя или пароль.')

    auth_page.auth_form_is_displayed()
    auth_page.check_url(f'{os.getenv("BASE_URL_UI")}/user/login')

def test_logout(authenticated_user_page: Page):
    dashboard_page = DashboardPage(authenticated_user_page)
    auth_page = AuthPage(authenticated_user_page)

    dashboard_page.open()
    dashboard_page.profile_menu_button_is_displayed()

    dashboard_page.click_profile_menu_button()
    dashboard_page.menu_exit_button_is_displayed()

    dashboard_page.click_menu_exit_button()
    auth_page.header_registration_button_is_displayed()
    auth_page.header_login_button_is_displayed()
    auth_page.check_url(f'{os.getenv("BASE_URL_UI")}/')

