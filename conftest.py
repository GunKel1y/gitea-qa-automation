import os
import pytest

from pathlib import Path
from dotenv import load_dotenv

from playwright.sync_api import Page, Browser

from helpers.api_client import create_user, delete_user, create_repo, delete_repo
from helpers.test_data import random_login, random_password, random_email, random_repo_name

load_dotenv(Path(__file__).parent / ".env")

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {**browser_context_args,
            "viewport": {"width": 1920, "height": 1080},
            "locale": "ru-RU"
            }

@pytest.fixture()
def test_user():
    login = random_login()
    password = random_password()
    email = random_email()
    create_user(username=login, email=email, password=password, must_change_password=False)
    yield {"login": login, "password": password, "email": email}
    delete_user(login)

@pytest.fixture()
def authenticated_user_page(browser: Browser, browser_context_args, test_user):

    context = browser.new_context(**browser_context_args)
    context.add_cookies([{
        "name": "lang", "value": "ru-RU",
        "domain": "localhost", "path": "/"
    }])

    context.request.post(f"{os.getenv('BASE_URL_UI')}/user/login", form={
        "user_name": test_user["login"],
        "password": test_user["password"],
    })

    page = context.new_page()

    yield page

    context.close()

@pytest.fixture()
def delete_user_after_registration(page: Page):
    user_login = random_login()
    user_password = random_password()
    user_email = random_email()

    yield [user_login, user_password, user_email]

    delete_user(user_login)

@pytest.fixture()
def register_person_for_auth(page: Page):
    test_user_login = random_login()
    test_user_pass = random_password()
    test_user_email = random_email()

    create_user(username=test_user_login, password=test_user_pass, email=test_user_email, must_change_password=False)

    page.goto(f"{os.getenv('BASE_URL_UI')}/user/login")

    yield [test_user_login, test_user_pass, test_user_email]

    delete_user(test_user_login)

@pytest.fixture()
def created_repo(authenticated_user_page, test_user):
    repo_name = random_repo_name()
    create_repo(owner=test_user["login"], repo_name=repo_name)

    yield {"repo_name": repo_name}

    delete_repo(owner=test_user["login"], repo_name=repo_name)
