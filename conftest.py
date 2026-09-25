import os
import pytest

from pathlib import Path
from dotenv import load_dotenv

from playwright.sync_api import Page, Browser

from helpers.api_client import create_user, delete_user, create_repo, delete_repo, create_organization, \
    delete_organization, create_organization_by_user, create_user_token
from helpers.test_data import random_login, random_password, random_email, random_repo_name

load_dotenv(Path(__file__).parent / ".env")

def _login_context(*, browser, browser_context_args, user):
    context = browser.new_context(**browser_context_args)
    context.add_cookies([{"name": "lang", "value": "ru-RU", "domain": "localhost", "path": "/"}])
    rspns = context.request.post(f"{os.getenv('BASE_URL_UI')}/user/login", form={
        "user_name": user["login"],
        "password": user["password"],
    })
    assert rspns.ok and "/user/login" not in rspns.url, f"Login failed: {rspns.status} {rspns.url}"
    return context

def _make_user() -> dict:
    user = {"login": random_login(), "password": random_password(), "email": random_email()}
    create_user(username=user["login"], email=user["email"], password=user["password"])
    return user

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {**browser_context_args,
            "viewport": {"width": 1920, "height": 1080},
            "locale": "ru-RU"
            }

@pytest.fixture()
def test_user():
    user = _make_user()
    yield {"login": user["login"], "password": user["password"], "email": user["email"]}
    delete_user(user["login"])

@pytest.fixture()
def authenticated_user_page(browser: Browser, browser_context_args, test_user):
    context = _login_context(browser=browser, browser_context_args=browser_context_args, user=test_user)
    yield context.new_page()
    context.close()

@pytest.fixture()
def second_test_user():
    user = _make_user()
    yield {"login": user["login"], "password": user["password"], "email": user["email"]}
    delete_user(user["login"])

@pytest.fixture()
def authenticated_second_user_page(browser: Browser, browser_context_args, second_test_user):
    context = _login_context(browser=browser, browser_context_args=browser_context_args, user=second_test_user)
    yield context.new_page()
    context.close()

@pytest.fixture()
def delete_user_after_registration(page: Page):
    user = {"login": random_login(), "password": random_password(), "email": random_email()}
    yield user
    delete_user(user["login"])

@pytest.fixture()
def created_public_repo(test_user):
    repo_name = random_repo_name()
    create_repo(owner=test_user["login"], repo_name=repo_name, private=False)

    yield {"repo_name": repo_name}

    delete_repo(owner=test_user["login"], repo_name=repo_name)

@pytest.fixture()
def created_private_repo(test_user):
    repo_name = random_repo_name()
    create_repo(owner=test_user["login"], repo_name=repo_name, private=True)

    yield {"repo_name": repo_name}

    delete_repo(owner=test_user["login"], repo_name=repo_name)

@pytest.fixture()
def created_public_organization_by_user(test_user):
    org_name = random_login()

    token_resp = create_user_token(
        username=test_user["login"],
        password=test_user["password"],
        scopes=["write:organization"]
    )
    assert token_resp.ok, f"Ошибка создания токена: {token_resp.status_code} {token_resp.text}"
    user_token = token_resp.json()["sha1"]

    org_resp = create_organization_by_user(org_name=org_name, visibility="public", user_token=user_token)
    assert org_resp.ok, f"Ошибка создания организации: {org_resp.status_code} {org_resp.text}"

    yield {"name": org_name}

    delete_organization(org_name)