from pathlib import Path
from uuid import uuid4
import os
from playwright.sync_api import Page, expect
import pytest
import requests as req
from dotenv import load_dotenv

TEST_LOGIN = 'test_username-' + str(uuid4())[:20]

load_dotenv(Path(__file__).parent / ".env")

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {**browser_context_args, "locale": "ru-RU"}

@pytest.fixture()
def register_page(page: Page):
    page.goto(f"{os.getenv('BASE_URL_UI')}/user/sign_up")
    yield
    req.delete(f"{os.getenv('BASE_API_URL')}/admin/users/" + TEST_LOGIN,
               headers={"Authorization": f"token {os.getenv("ADMIN_TOKEN")}"},
               params='purge=true')

@pytest.fixture()
def register_person_for_auth(page: Page):
    test_user_login = 'user-' + str(uuid4())[:7] + '-test'
    test_user_pass = 'user-' + str(uuid4())[:7] + '-pass'
    test_user_email = test_user_login + "@123.com"

    req.post(f"{os.getenv('BASE_API_URL')}/admin/users/",
             headers={"Authorization": f"token {os.getenv('ADMIN_TOKEN')}"},
             json={
                 "email": test_user_email,
                 "password": test_user_pass,
                 "username": test_user_login,
                 "must_change_password": False
             })

    page.goto(f"{os.getenv('BASE_URL_UI')}/user/login")

    yield [test_user_login, test_user_pass, test_user_email]

    req.delete(f"{os.getenv('BASE_API_URL')}/admin/users/" + test_user_login,
               headers={"Authorization": f"token {os.getenv('ADMIN_TOKEN')}"},
               params='purge=true')