import os

from playwright.sync_api import Page, expect
from uuid import uuid4

from conftest import TEST_LOGIN
from pages.register_page import RegisterPage
from pages.dashboard_page import DashboardPage

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

