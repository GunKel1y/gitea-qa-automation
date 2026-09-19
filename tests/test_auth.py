import os

from playwright.sync_api import Page, expect
from pages.auth_page import AuthPage
from pages.dashboard_page import DashboardPage

from helpers.test_data import random_password

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

def test_login_with_invalid_password(page: Page, register_person_for_auth):
    auth_page = AuthPage(page)
    person_username = register_person_for_auth[0]
    invalid_password = random_password()

    auth_page.auth_form_is_displayed()

    auth_page.fill_username(person_username)
    auth_page.check_value_username(person_username)

    auth_page.fill_password(invalid_password)
    auth_page.check_value_password(invalid_password)

    auth_page.click_login_button()

    auth_page.error_message_is_displayed()
    auth_page.check_negative_message_text('Неверное имя пользователя или пароль.')