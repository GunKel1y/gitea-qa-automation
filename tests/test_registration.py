import os
import pytest

from playwright.sync_api import Page

from pages.registration_page import RegisterPage
from pages.dashboard_page import DashboardPage

from helpers.test_data import random_email, random_password, random_login, password_with_length


def test_register_with_truth_creds(page: Page, delete_user_after_registration):
    register_page = RegisterPage(page)
    dashboard_page = DashboardPage(page)

    register_page.open()

    register_page.registration_form_is_displayed()

    register_page.fill_username(delete_user_after_registration[0])
    register_page.check_username_value(delete_user_after_registration[0])

    register_page.fill_email(delete_user_after_registration[2])
    register_page.check_email_value(delete_user_after_registration[2])

    register_page.fill_password(delete_user_after_registration[1])
    register_page.check_password_value(delete_user_after_registration[1])

    register_page.fill_doublecheck_password(delete_user_after_registration[1])
    register_page.check_doublecheck_password_value(delete_user_after_registration[1])

    register_page.click_registration_button()

    dashboard_page.dashboard_is_displayed()
    dashboard_page.success_registration_banner_is_displayed()
    dashboard_page.check_success_registration_banner_text('Учётная запись успешно создана. Добро пожаловать!')
    dashboard_page.check_url(f'{os.getenv("BASE_URL_UI")}/')

@pytest.mark.parametrize("case",
                         ["in_use_username", "in_use_email", "invalid_email",
                          "failed_confirm_pass", "min_length_pass", "max_length_pass"])
def test_registration_with_invalid_creds(page: Page, test_user, case):
    registration_page = RegisterPage(page)

    person_username = random_login()
    person_email = random_email()
    person_password = random_password()

    if case == "in_use_username":
        person_username = test_user["login"]
        error_message = "Имя пользователя уже занято."
    elif case == "in_use_email":
        person_email = test_user["email"]
        error_message = "Этот адрес электронной почты уже используется."
    elif case == "invalid_email":
        person_email = random_login()
        error_message = None
    elif case == "failed_confirm_pass":
        error_message = "Пароли не совпадают."
    elif case == "min_length_pass":
        person_password = person_password[:7]
        error_message = "Пароль не может быть короче 8 символов."
    else:
        person_password = password_with_length(256)
        error_message = "Пароль должен содержать максимум 255 символов."

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
