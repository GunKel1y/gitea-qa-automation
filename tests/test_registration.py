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


pytestmark = allure.epic("Регистрация")


@pytest.mark.parametrize(
    "invalid_email, title",
    [
        pytest.param(
            "",
            "Регистрация с пустым email",
            id="empty_value",
            marks=[pytest.mark.p2, allure.testcase("TC-A-036"), allure.severity(allure.severity_level.NORMAL)],
        ),
        pytest.param(
            unique_name(),
            "Регистрация с email без @",
            id="no_symbol",
            marks=[pytest.mark.p2, allure.testcase("TC-A-023"), allure.severity(allure.severity_level.NORMAL)],
        ),
        pytest.param(
            f"{unique_name()}@",
            "Регистрация с email без домена (name@)",
            id="no_domain",
            marks=[pytest.mark.p2, allure.testcase("TC-A-037"), allure.severity(allure.severity_level.NORMAL)],
        ),
        pytest.param(
            f"@{unique_name()}.com",
            "Регистрация с email без локальной части (@name.com)",
            id="no_local",
            marks=[pytest.mark.p2, allure.testcase("TC-A-038"), allure.severity(allure.severity_level.NORMAL)],
        ),
        pytest.param(
            email_with_length(length=247, domain="@test.ru"),
            "Регистрация с email длиннее максимума (255 символов)",
            id="above_max",
            marks=[pytest.mark.p3, allure.testcase("TC-A-040"), allure.severity(allure.severity_level.MINOR)],
        ),
    ],
)
@allure.title("{title}")
def test_registration_with_invalid_email_format(page: Page, invalid_email, title):
    registration_page = RegisterPage(page)
    user_login = unique_name(prefix="user")
    person_password = random_password()

    with allure.step("Зарегистрироваться с невалидным email"):
        registration_page.open()
        registration_page.fill_username(user_login)
        registration_page.fill_email(invalid_email)
        registration_page.fill_password(person_password)
        registration_page.fill_doublecheck_password(person_password)

        registration_page.click_registration_button()

    with allure.step("Проверить, что регистрация отклонена"):
        registration_page.check_url("/user/sign_up")
        if len(invalid_email) > 254:
            registration_page.error_message_has_text("Адрес эл. почты должен содержать максимум 254 символов.")

    with allure.step("Проверить, что пользователь не создан"):
        registration_page.open_profile_user(user_login)

        not_found_page = NotFoundErrorPage(page)
        not_found_page.check_title_text()
        not_found_page.check_description_text()


@pytest.mark.parametrize(
    "delete_user_after_registration, title",
    [
        pytest.param(
            None,
            "Успешная регистрация нового юзера",
            id="unique_creds",
            marks=[pytest.mark.p1, allure.testcase("TC-A-010"), allure.severity(allure.severity_level.CRITICAL)],
        ),
        pytest.param(
            (unique_name(prefix="user"), value_with_length(8), random_email()),
            "Регистрация с паролем минимальной валидной длины (8 символов)",
            id="minimum_password_length",
            marks=[pytest.mark.p3, allure.testcase("TC-A-027"), allure.severity(allure.severity_level.MINOR)],
        ),
        pytest.param(
            (unique_name(prefix="user"), value_with_length(255), random_email()),
            "Регистрация с паролем максимальной валидной длины (255 символов)",
            id="upper_limit_password",
            marks=[pytest.mark.p3, allure.testcase("TC-A-028"), allure.severity(allure.severity_level.MINOR)],
        ),
        pytest.param(
            (unique_name(prefix="user"), random_password(), email_with_length(length=246, domain="@test.ru")),
            "Регистрация с email максимальной валидной длины (254 символа)",
            id="upper_limit_email",
            marks=[pytest.mark.p3, allure.testcase("TC-A-039"), allure.severity(allure.severity_level.MINOR)],
        ),
        pytest.param(
            (unique_name(prefix="user"), random_password(), email_with_length(length=1, domain="@ru")),
            "Регистрация с минимально короткой записью email (1@ru)",
            id="minimum_email_length",
            marks=[pytest.mark.p3, allure.testcase("TC-A-041"), allure.severity(allure.severity_level.MINOR)],
        ),
        pytest.param(
            (value_with_length(length=1), random_password(), random_email()),
            "Username из 1 символа (минимального ограничения длины нет)",
            id="minimum_username_length",
            marks=[pytest.mark.p3, allure.testcase("TC-A-034a"), allure.severity(allure.severity_level.MINOR)],
        ),
        pytest.param(
            (value_with_length(length=40), random_password(), random_email()),
            "Username максимальной длины (40 символов)",
            id="upper_limit_username",
            marks=[pytest.mark.p3, allure.testcase("TC-A-034b"), allure.severity(allure.severity_level.MINOR)],
        ),
    ],
    indirect=["delete_user_after_registration"],
)
@allure.title("{title}")
def test_register_with_valid_creds(page: Page, delete_user_after_registration, title):
    register_page = RegisterPage(page)
    dashboard_page = DashboardPage(page)
    username = delete_user_after_registration["login"]
    email = delete_user_after_registration["email"]
    password = delete_user_after_registration["password"]

    with allure.step("Зарегистрироваться с валидными данными"):
        register_page.open()

        register_page.fill_username(username)
        register_page.fill_email(email)
        register_page.fill_password(password)
        register_page.fill_doublecheck_password(password)

        register_page.click_registration_button()

    with allure.step("Проверить успешную регистрацию"):
        dashboard_page.dashboard_is_displayed()
        dashboard_page.check_success_registration_banner_text("Учётная запись успешно создана. Добро пожаловать!")
        dashboard_page.check_url("/")


@pytest.mark.parametrize(
    "taken_field, expected_error, title",
    [
        pytest.param(
            "login",
            "Имя пользователя уже занято.",
            "Регистрация с уже занятым username",
            id="in_use_username",
            marks=[pytest.mark.p2, allure.testcase("TC-A-022"), allure.severity(allure.severity_level.NORMAL)],
        ),
        pytest.param(
            "email",
            "Этот адрес электронной почты уже используется.",
            "Регистрация с уже используемым email другим юзером",
            id="in_use_email",
            marks=[pytest.mark.p3, allure.testcase("TC-A-031"), allure.severity(allure.severity_level.MINOR)],
        ),
    ],
)
@allure.title("{title}")
def test_registration_with_taken_login_or_email(page: Page, test_user, taken_field, expected_error, title):
    registration_page = RegisterPage(page)
    new_user = {"login": unique_name(prefix="user"), "email": random_email(), "password": random_password()}
    new_user[taken_field] = test_user[taken_field]

    with allure.step("Зарегистрироваться с занятым логином или email"):
        registration_page.open()
        registration_page.fill_username(new_user["login"])
        registration_page.fill_email(new_user["email"])
        registration_page.fill_password(new_user["password"])
        registration_page.fill_doublecheck_password(new_user["password"])
        registration_page.click_registration_button()

    with allure.step("Проверить, что регистрация отклонена"):
        registration_page.error_message_has_text(expected_error)
        registration_page.check_url("/user/sign_up")


SHORT_PASSWORD = value_with_length(7)
LONG_PASSWORD = value_with_length(256)


@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.p2
@pytest.mark.parametrize(
    "password, confirm, expected_error, title",
    [
        pytest.param(
            random_password(),
            random_password(),
            "Пароли не совпадают.",
            "Регистрация с несовпадающими password/confirm",
            id="failed_confirm_pass",
            marks=allure.testcase("TC-A-024"),
        ),
        pytest.param(
            SHORT_PASSWORD,
            SHORT_PASSWORD,
            "Пароль не может быть короче 8 символов.",
            "Регистрация с паролем короче минимальной длины (7 символов при минимуме 8)",
            id="min_length_pass",
            marks=allure.testcase("TC-A-025"),
        ),
        pytest.param(
            LONG_PASSWORD,
            LONG_PASSWORD,
            "Пароль должен содержать максимум 255 символов.",
            "Регистрация с паролем длиннее максимума (256 символов)",
            id="max_length_pass",
            marks=allure.testcase("TC-A-026"),
        ),
    ],
)
@allure.title("{title}")
def test_registration_with_invalid_password(page: Page, password, confirm, expected_error, title):
    registration_page = RegisterPage(page)

    with allure.step("Зарегистрироваться с невалидным паролем"):
        registration_page.open()
        registration_page.fill_username(unique_name(prefix="user"))
        registration_page.fill_email(random_email())
        registration_page.fill_password(password)
        registration_page.fill_doublecheck_password(confirm)
        registration_page.click_registration_button()

    with allure.step("Проверить, что регистрация отклонена"):
        registration_page.error_message_has_text(expected_error)
        registration_page.check_url("/user/sign_up")


@allure.testcase("TC-A-033")
@allure.title("Регистрация с недопустимыми символами в username (пробел, эмодзи, /)")
@allure.severity(allure.severity_level.NORMAL)
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

    with allure.step("Зарегистрироваться с недопустимыми символами в логине"):
        registration_page.open()
        registration_page.fill_username(username_value)
        registration_page.fill_email(random_email())
        registration_page.fill_password(password)
        registration_page.fill_doublecheck_password(password)
        registration_page.click_registration_button()

    with allure.step("Проверить, что регистрация отклонена"):
        registration_page.error_message_has_text("""
    Пользователь can only contain alphanumeric characters ('0-9','a-z','A-Z'), dash ('-'),
    underscore ('_') and dot ('.'). It cannot begin or end with non-alphanumeric characters,
    and consecutive non-alphanumeric characters are also forbidden.
    """)
        registration_page.check_url("/user/sign_up")


@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.p2
@pytest.mark.parametrize(
    "username, password, validation_method, title",
    [
        pytest.param(
            "",
            random_password(),
            RegisterPage.check_show_error_in_required_username,
            "Регистрация с пустым username",
            id="empty_username",
            marks=allure.testcase("TC-A-032"),
        ),
        pytest.param(
            unique_name(prefix="user"),
            "",
            RegisterPage.check_show_error_in_required_password,
            "Регистрация с пустым паролем",
            id="empty_password",
            marks=allure.testcase("TC-A-035"),
        ),
    ],
)
@allure.title("{title}")
def test_registration_with_empty_value_in_fields(page: Page, username, password, validation_method, title):
    registration_page = RegisterPage(page)

    with allure.step("Зарегистрироваться с пустым обязательным полем"):
        registration_page.open()
        registration_page.fill_username(username)
        registration_page.fill_email(random_email())
        registration_page.fill_password(password)
        registration_page.fill_doublecheck_password(password)
        registration_page.click_registration_button()

    with allure.step("Проверить, что регистрация отклонена"):
        validation_method(registration_page)
        registration_page.check_url("/user/sign_up")


@allure.testcase("TC-A-034c")
@allure.title("Username длиннее максимума (41 символ)")
@allure.severity(allure.severity_level.MINOR)
@pytest.mark.p3
def test_registration_with_username_exceeding_max_length(page: Page, delete_user_after_registration):
    register_page = RegisterPage(page)
    not_found_page = NotFoundErrorPage(page)
    delete_user_after_registration["login"] = value_with_length(length=41)
    password = delete_user_after_registration["password"]

    with allure.step("Зарегистрироваться с логином длиннее максимума"):
        register_page.open()

        register_page.fill_username(delete_user_after_registration["login"])
        register_page.fill_email(delete_user_after_registration["email"])
        register_page.fill_password(password)
        register_page.fill_doublecheck_password(password)

        register_page.click_registration_button()

    with allure.step("Проверить, что регистрация отклонена"):
        register_page.error_message_has_text("Пользователь должен содержать максимум 40 символов.")
        register_page.check_url("/user/sign_up")

    with allure.step("Проверить, что пользователь не создан"):
        register_page.open_profile_user(delete_user_after_registration["login"])
        not_found_page.check_title_text()
        not_found_page.check_description_text()
