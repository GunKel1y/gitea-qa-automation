import pytest

from playwright.sync_api import Page

from pages.registration_page import RegisterPage
from pages.dashboard_page import DashboardPage

from helpers.test_data import random_email, random_password, password_with_length, unique_name


@pytest.mark.parametrize("invalid_email", [
    pytest.param('', id="no_symbol"),
    pytest.param(f"{unique_name()}@", id="no_domain"),
    pytest.param(f"@{unique_name()}.com", id="no_local"),
])
def test_registration_with_invalid_email_format(page: Page, invalid_email):
    registration_page = RegisterPage(page)
    person_password = random_password()

    registration_page.open()
    registration_page.fill_username(unique_name(prefix='user'))
    registration_page.fill_email(invalid_email)
    registration_page.fill_password(person_password)
    registration_page.fill_doublecheck_password(person_password)

    registration_page.click_registration_button()

    registration_page.check_url("/user/sign_up")

def test_register_with_valid_creds(page: Page, delete_user_after_registration):
    register_page = RegisterPage(page)
    dashboard_page = DashboardPage(page)

    register_page.open()

    register_page.fill_username(delete_user_after_registration["login"])
    register_page.fill_email(delete_user_after_registration["email"])
    register_page.fill_password(delete_user_after_registration["password"])
    register_page.fill_doublecheck_password(delete_user_after_registration["password"])

    register_page.click_registration_button()

    dashboard_page.dashboard_is_displayed()
    dashboard_page.check_success_registration_banner_text('Учётная запись успешно создана. Добро пожаловать!')
    dashboard_page.check_url('/')

@pytest.mark.parametrize("taken_field, expected_error", [
    pytest.param("login", "Имя пользователя уже занято.", id="in_use_username"),
    pytest.param("email", "Этот адрес электронной почты уже используется.", id="in_use_email"),
])
def test_registration_with_taken_login_or_email(page: Page, test_user, taken_field, expected_error):
    registration_page = RegisterPage(page)
    new_user = {"login": unique_name(prefix='user'), "email": random_email(), "password": random_password()}
    new_user[taken_field] = test_user[taken_field]

    registration_page.open()
    registration_page.fill_username(new_user["login"])
    registration_page.fill_email(new_user["email"])
    registration_page.fill_password(new_user["password"])
    registration_page.fill_doublecheck_password(new_user["password"])
    registration_page.click_registration_button()

    registration_page.error_message_has_text(expected_error)
    registration_page.check_url("/user/sign_up")

SHORT_PASSWORD = password_with_length(7)
LONG_PASSWORD = password_with_length(256)

@pytest.mark.parametrize("password, confirm, expected_error", [
    pytest.param(random_password(), random_password(), "Пароли не совпадают.", id="failed_confirm_pass"),
    pytest.param(SHORT_PASSWORD, SHORT_PASSWORD, "Пароль не может быть короче 8 символов.", id="min_length_pass"),
    pytest.param(LONG_PASSWORD, LONG_PASSWORD, "Пароль должен содержать максимум 255 символов.", id="max_length_pass"),
])
def test_registration_with_invalid_password(page: Page, password, confirm, expected_error):
    registration_page = RegisterPage(page)

    registration_page.open()
    registration_page.fill_username(unique_name(prefix='user'))
    registration_page.fill_email(random_email())
    registration_page.fill_password(password)
    registration_page.fill_doublecheck_password(confirm)
    registration_page.click_registration_button()

    registration_page.error_message_has_text(expected_error)
    registration_page.check_url("/user/sign_up")