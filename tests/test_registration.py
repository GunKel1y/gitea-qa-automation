import os

from playwright.sync_api import Page, expect
from uuid import uuid4

from conftest import TEST_LOGIN
from pages.register_page import RegisterPage
from pages.dashboard_page import DashboardPage

from helpers.test_data import random_email, random_password

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

def test_registration_with_exist_username(page: Page, register_person_for_auth):
    registration_page = RegisterPage(page)
    person_username = register_person_for_auth[0]
    person_password = random_password()
    person_email = random_email()

    registration_page.open()
    registration_page.registration_form_is_displayed()

    registration_page.fill_username(person_username)
    registration_page.check_username_value(person_username)

    registration_page.fill_email(person_email)
    registration_page.check_email_value(person_email)

    registration_page.fill_password(person_password)
    registration_page.check_password_value(person_password)

    registration_page.fill_doublecheck_password(person_password)
    registration_page.check_doublecheck_password_value(person_password)

    registration_page.click_registration_button()

    registration_page.error_message_is_displayed()
    registration_page.check_error_message_text("Имя пользователя уже занято.")
    registration_page.check_url(f"{os.getenv('BASE_URL_UI')}/user/sign_up")
