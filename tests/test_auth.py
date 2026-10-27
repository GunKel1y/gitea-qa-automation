import allure
import pytest
from playwright.sync_api import Page

from helpers.test_data import random_password, unique_name
from pages.auth_page import AuthPage
from pages.dashboard_page import DashboardPage
from pages.repo.create_repository_page import CreateRepositoryPage


pytestmark = allure.epic("Авторизация")


@allure.testcase("TC-A-001")
@allure.title("Успешный логин с валидными данными")
@allure.severity(allure.severity_level.BLOCKER)
@pytest.mark.p0
def test_login_with_valid_creds(page: Page, test_user):
    auth_page = AuthPage(page)
    dashboard_page = DashboardPage(page)
    with allure.step("Войти с валидными данными"):
        auth_page.open()

        person_login = test_user["login"]
        person_pass = test_user["password"]

        auth_page.fill_username(person_login)
        auth_page.fill_password(person_pass)
        auth_page.click_login_button()

    with allure.step("Проверить, что пользователь авторизован"):
        auth_page.check_url("/")
        dashboard_page.dashboard_is_displayed()
        dashboard_page.global_header.profile_menu_button_is_displayed()
        dashboard_page.switch_user_button_is_displayed()
        dashboard_page.switch_user_image_is_displayed()


@pytest.mark.parametrize(
    "case, title",
    [
        pytest.param(
            "invalid_password",
            "Логин с неверным паролем",
            marks=[pytest.mark.p2, allure.testcase("TC-A-020"), allure.severity(allure.severity_level.NORMAL)],
        ),
        pytest.param(
            "non_exist_creds",
            "Логин с несуществующим username",
            marks=[pytest.mark.p2, allure.testcase("TC-A-021"), allure.severity(allure.severity_level.NORMAL)],
        ),
    ],
)
@allure.title("{title}")
def test_login_with_invalid_creds(page: Page, test_user, case, title):
    auth_page = AuthPage(page)
    with allure.step("Попытаться войти с неверными данными"):
        auth_page.open()

        if case == "invalid_password":
            person_login, person_password = test_user["login"], test_user["password"] + "invalid"
        else:
            person_login, person_password = unique_name(prefix="user"), random_password()

        auth_page.fill_username(person_login)
        auth_page.fill_password(person_password)

        auth_page.click_login_button()

    with allure.step("Проверить, что вход отклонен"):
        auth_page.error_message_has_text("Неверное имя пользователя или пароль.")

        auth_page.auth_form_is_displayed()
        auth_page.check_url("/user/login")


@allure.testcase("TC-A-030")
@allure.title("Логин с пустыми полями")
@allure.severity(allure.severity_level.MINOR)
@pytest.mark.p3
def test_login_with_empty_fields(page: Page):
    auth_page = AuthPage(page)
    with allure.step("Попытаться войти с пустыми полями"):
        auth_page.open()

        auth_page.auth_form_is_displayed()

        auth_page.click_login_button()

    with allure.step("Проверить, что вход не выполнен"):
        auth_page.auth_form_is_displayed()
        auth_page.check_url("/user/login")


@allure.testcase("TC-A-002")
@allure.title("Логаут")
@allure.severity(allure.severity_level.BLOCKER)
@pytest.mark.p0
def test_logout(authenticated_user_page: Page):
    dashboard_page = DashboardPage(authenticated_user_page)
    auth_page = AuthPage(authenticated_user_page)

    with allure.step("Выйти из аккаунта"):
        dashboard_page.open()

        dashboard_page.global_header.click_profile_menu_button()

        dashboard_page.global_header.click_menu_exit_button()
    with allure.step("Проверить, что пользователь вышел"):
        auth_page.global_header.registration_button_is_displayed()
        auth_page.global_header.login_button_is_displayed()
        auth_page.check_url("/")
        auth_page.open_user_settings()
        auth_page.check_url("/user/login?redirect_to=%2Fuser%2Fsettings")


@allure.testcase("TC-A-011")
@allure.title("Доступ к защищённой странице без авторизации отклонён")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.p1
def test_access_page_without_auth_is_denied(page: Page):
    auth_page = AuthPage(page)
    create_repo_page = CreateRepositoryPage(page)

    with allure.step("Открыть страницу создания репозитория без авторизации"):
        create_repo_page.open()
    with allure.step("Проверить перенаправление на страницу входа"):
        auth_page.check_url("/user/login?redirect_to=%2Frepo%2Fcreate")
        auth_page.auth_form_is_displayed()
