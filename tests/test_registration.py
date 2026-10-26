import allure
import pytest
from playwright.sync_api import Page

from helpers.test_data import (
    email_with_length,
    random_email,
    random_password,
    unique_name,
    value_with_length,
)
from pages.dashboard_page import DashboardPage
from pages.not_found_error_page import NotFoundErrorPage
from pages.registration_page import RegisterPage


@pytest.mark.parametrize(
    "invalid_email",
    [
        pytest.param("", id="empty_value", marks=[pytest.mark.p2, allure.testcase("TC-A-036")]),
        pytest.param(unique_name(), id="no_symbol", marks=[pytest.mark.p2, allure.testcase("TC-A-023")]),
        pytest.param(f"{unique_name()}@", id="no_domain", marks=[pytest.mark.p2, allure.testcase("TC-A-037")]),
        pytest.param(f"@{unique_name()}.com", id="no_local", marks=[pytest.mark.p2, allure.testcase("TC-A-038")]),
        pytest.param(
            email_with_length(length=247, domain="@test.ru"),
            id="above_max",
            marks=[pytest.mark.p3, allure.testcase("TC-A-040")],
        ),
    ],
)
def test_registration_with_invalid_email_format(page: Page, invalid_email):
    registration_page = RegisterPage(page)
    user_login = unique_name(prefix="user")
    person_password = random_password()

    registration_page.open()
    registration_page.fill_username(user_login)
    registration_page.fill_email(invalid_email)
    registration_page.fill_password(person_password)
    registration_page.fill_doublecheck_password(person_password)

    registration_page.click_registration_button()

    registration_page.check_url("/user/sign_up")
    if len(invalid_email) > 254:
        registration_page.error_message_has_text("Адрес эл. почты должен содержать максимум 254 символов.")

    registration_page.open_profile_user(user_login)

    not_found_page = NotFoundErrorPage(page)
    not_found_page.check_title_text()
    not_found_page.check_description_text()


@pytest.mark.parametrize(
    "delete_user_after_registration",
    [
        pytest.param(None, id="unique_creds", marks=[pytest.mark.p1, allure.testcase("TC-A-010")]),
        pytest.param(
            (unique_name(prefix="user"), value_with_length(8), random_email()),
            id="minimum_password_length",
            marks=[pytest.mark.p3, allure.testcase("TC-A-027")],
        ),
        pytest.param(
            (unique_name(prefix="user"), value_with_length(255), random_email()),
            id="upper_limit_password",
            marks=[pytest.mark.p3, allure.testcase("TC-A-028")],
        ),
        pytest.param(
            (unique_name(prefix="user"), random_password(), email_with_length(length=246, domain="@test.ru")),
            id="upper_limit_email",
            marks=[pytest.mark.p3, allure.testcase("TC-A-039")],
        ),
        pytest.param(
            (unique_name(prefix="user"), random_password(), email_with_length(length=1, domain="@ru")),
            id="minimum_email_length",
            marks=[pytest.mark.p3, allure.testcase("TC-A-041")],
        ),
        pytest.param(
            (value_with_length(length=1), random_password(), random_email()),
            id="minimum_username_length",
            marks=[pytest.mark.p3, allure.testcase("TC-A-034a")],
        ),
        pytest.param(
            (value_with_length(length=40), random_password(), random_email()),
            id="upper_limit_username",
            marks=[pytest.mark.p3, allure.testcase("TC-A-034b")],
        ),
    ],
    indirect=["delete_user_after_registration"],
)
def test_register_with_valid_creds(page: Page, delete_user_after_registration):
    register_page = RegisterPage(page)
    dashboard_page = DashboardPage(page)
    username = delete_user_after_registration["login"]
    email = delete_user_after_registration["email"]
    password = delete_user_after_registration["password"]

    register_page.open()

    register_page.fill_username(username)
    register_page.fill_email(email)
    register_page.fill_password(password)
    register_page.fill_doublecheck_password(password)

    register_page.click_registration_button()

    dashboard_page.dashboard_is_displayed()
    dashboard_page.check_success_registration_banner_text("Учётная запись успешно создана. Добро пожаловать!")
    dashboard_page.check_url("/")


@pytest.mark.parametrize(
    "taken_field, expected_error",
    [
        pytest.param(
            "login",
            "Имя пользователя уже занято.",
            id="in_use_username",
            marks=[pytest.mark.p2, allure.testcase("TC-A-022")],
        ),
        pytest.param(
            "email",
            "Этот адрес электронной почты уже используется.",
            id="in_use_email",
            marks=[pytest.mark.p3, allure.testcase("TC-A-031")],
        ),
    ],
)
def test_registration_with_taken_login_or_email(page: Page, test_user, taken_field, expected_error):
    registration_page = RegisterPage(page)
    new_user = {"login": unique_name(prefix="user"), "email": random_email(), "password": random_password()}
    new_user[taken_field] = test_user[taken_field]

    registration_page.open()
    registration_page.fill_username(new_user["login"])
    registration_page.fill_email(new_user["email"])
    registration_page.fill_password(new_user["password"])
    registration_page.fill_doublecheck_password(new_user["password"])
    registration_page.click_registration_button()

    registration_page.error_message_has_text(expected_error)
    registration_page.check_url("/user/sign_up")


SHORT_PASSWORD = value_with_length(7)
LONG_PASSWORD = value_with_length(256)


@pytest.mark.p2
@pytest.mark.parametrize(
    "password, confirm, expected_error",
    [
        pytest.param(
            random_password(),
            random_password(),
            "Пароли не совпадают.",
            id="failed_confirm_pass",
            marks=allure.testcase("TC-A-024"),
        ),
        pytest.param(
            SHORT_PASSWORD,
            SHORT_PASSWORD,
            "Пароль не может быть короче 8 символов.",
            id="min_length_pass",
            marks=allure.testcase("TC-A-025"),
        ),
        pytest.param(
            LONG_PASSWORD,
            LONG_PASSWORD,
            "Пароль должен содержать максимум 255 символов.",
            id="max_length_pass",
            marks=allure.testcase("TC-A-026"),
        ),
    ],
)
def test_registration_with_invalid_password(page: Page, password, confirm, expected_error):
    registration_page = RegisterPage(page)

    registration_page.open()
    registration_page.fill_username(unique_name(prefix="user"))
    registration_page.fill_email(random_email())
    registration_page.fill_password(password)
    registration_page.fill_doublecheck_password(confirm)
    registration_page.click_registration_button()

    registration_page.error_message_has_text(expected_error)
    registration_page.check_url("/user/sign_up")


@allure.testcase("TC-A-033")
@pytest.mark.p2
@pytest.mark.parametrize(
    "username_value",
    [
        pytest.param(unique_name(prefix="😊test"), id="emoji"),
        pytest.param(unique_name(prefix="test/"), id="slash"),
        pytest.param(unique_name(prefix="te st"), id="space"),
    ],
)
def test_registration_with_invalid_characters_in_username(page: Page, username_value):
    password = random_password()
    registration_page = RegisterPage(page)

    registration_page.open()
    registration_page.fill_username(username_value)
    registration_page.fill_email(random_email())
    registration_page.fill_password(password)
    registration_page.fill_doublecheck_password(password)
    registration_page.click_registration_button()

    registration_page.error_message_has_text("""
    Пользователь can only contain alphanumeric characters ('0-9','a-z','A-Z'), dash ('-'),
    underscore ('_') and dot ('.'). It cannot begin or end with non-alphanumeric characters,
    and consecutive non-alphanumeric characters are also forbidden.
    """)
    registration_page.check_url("/user/sign_up")


@pytest.mark.p2
@pytest.mark.parametrize(
    "username, password, validation_method",
    [
        pytest.param(
            "",
            random_password(),
            RegisterPage.check_show_error_in_required_username,
            id="empty_username",
            marks=allure.testcase("TC-A-032"),
        ),
        pytest.param(
            unique_name(prefix="user"),
            "",
            RegisterPage.check_show_error_in_required_password,
            id="empty_password",
            marks=allure.testcase("TC-A-035"),
        ),
    ],
)
def test_registration_with_empty_value_in_fields(page: Page, username, password, validation_method):
    registration_page = RegisterPage(page)

    registration_page.open()
    registration_page.fill_username(username)
    registration_page.fill_email(random_email())
    registration_page.fill_password(password)
    registration_page.fill_doublecheck_password(password)
    registration_page.click_registration_button()

    validation_method(registration_page)
    registration_page.check_url("/user/sign_up")


@allure.testcase("TC-A-034c")
@pytest.mark.p3
def test_registration_with_username_exceeding_max_length(page: Page, delete_user_after_registration):
    register_page = RegisterPage(page)
    not_found_page = NotFoundErrorPage(page)
    delete_user_after_registration["login"] = value_with_length(length=41)
    password = delete_user_after_registration["password"]

    register_page.open()

    register_page.fill_username(delete_user_after_registration["login"])
    register_page.fill_email(delete_user_after_registration["email"])
    register_page.fill_password(password)
    register_page.fill_doublecheck_password(password)

    register_page.click_registration_button()

    register_page.error_message_has_text("Пользователь должен содержать максимум 40 символов.")
    register_page.check_url("/user/sign_up")

    register_page.open_profile_user(delete_user_after_registration["login"])
    not_found_page.check_title_text()
    not_found_page.check_description_text()
