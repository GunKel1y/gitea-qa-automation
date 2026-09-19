import os

import pytest

from playwright.sync_api import Page, expect
from uuid import uuid4

from conftest import TEST_LOGIN
from pages.registration_page import RegisterPage
from pages.dashboard_page import DashboardPage

from helpers.test_data import random_email, random_password, random_login

TEST_EMAIL = 'test-email-' + str(uuid4())[:20] + '@test.ru'
TEST_PASSWORD = str(uuid4())

def test_register_with_truth_creds(page: Page, register_page):
    register_page = RegisterPage(page)
    dashboard_page = DashboardPage(page)

    register_page.registration_form_is_displayed()

    register_page.fill_username(TEST_LOGIN)
    register_page.check_username_value(TEST_LOGIN)

    register_page.fill_email(TEST_EMAIL)
    register_page.check_email_value(TEST_EMAIL)

    register_page.fill_password(TEST_PASSWORD)
    register_page.check_password_value(TEST_PASSWORD)

    register_page.fill_doublecheck_password(TEST_PASSWORD)
    register_page.check_doublecheck_password_value(TEST_PASSWORD)

    register_page.click_registration_button()

    dashboard_page.dashboard_is_displayed()
    dashboard_page.success_registration_banner_is_displayed()
    dashboard_page.check_success_registration_banner_text('Учётная запись успешно создана. Добро пожаловать!')
    dashboard_page.check_url(f'{os.getenv("BASE_URL_UI")}/')

@pytest.mark.parametrize("case",
                         ["in_use_username", "in_use_email", "invalid_email", "failed_confirm_pass"])
def test_registration_with_invalid_creds(page: Page, register_person_for_auth, case):
    registration_page = RegisterPage(page)

    person_password = random_password()

    if case == "in_use_username":
        person_username = register_person_for_auth[0]
        person_email = random_email()
        error_message = "Имя пользователя уже занято."
    elif case == "in_use_email":
        person_username = random_login()
        person_email = register_person_for_auth[2]
        error_message = "Этот адрес электронной почты уже используется."
    elif case == "invalid_email":
        person_username = random_login()
        person_email = random_login()
        error_message = None
    else:
        person_username = random_login()
        person_email = random_email()
        error_message = "Пароли не совпадают."

    registration_page.open()
    registration_page.registration_form_is_displayed()

    registration_page.fill_username(person_username)
    registration_page.check_username_value(person_username)

    registration_page.fill_email(person_email)
    registration_page.check_email_value(person_email)

    registration_page.fill_password(person_password)
    registration_page.check_password_value(person_password)

    if case == "failed_confirm_pass":
        failed_confirm_pass = random_password()
        registration_page.fill_doublecheck_password(failed_confirm_pass)
        registration_page.check_doublecheck_password_value(failed_confirm_pass)
    else:
        registration_page.fill_doublecheck_password(person_password)
        registration_page.check_doublecheck_password_value(person_password)

    registration_page.click_registration_button()

    if case != "invalid_email":
        registration_page.error_message_is_displayed()
        registration_page.check_error_message_text(error_message)
    registration_page.registration_form_is_displayed()
    registration_page.check_url(f"{os.getenv('BASE_URL_UI')}/user/sign_up")
