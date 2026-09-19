from pathlib import Path
import re
from uuid import uuid4
import os
from playwright.sync_api import Page, Browser
import pytest
import requests as req
from dotenv import load_dotenv
from helpers.test_data import random_login, random_password, random_email
from pages.auth_page import AuthPage

TEST_LOGIN = 'test_username-' + str(uuid4())[:20]

load_dotenv(Path(__file__).parent / ".env")

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {**browser_context_args,
            "viewport": {"width": 1920, "height": 1080},
            "locale": "ru-RU"
            }

@pytest.fixture()
def authenticated_user_page(browser: Browser, browser_context_args):
    test_user_login = random_login()
    test_user_pass = random_password()
    test_user_email = random_email()

    req.post(f"{os.getenv('BASE_API_URL')}/admin/users/",
             headers={"Authorization": f"token {os.getenv('ADMIN_TOKEN')}"},
             json={
                 "email": test_user_email,
                 "password": test_user_pass,
                 "username": test_user_login,
                 "must_change_password": False
             })

    context = browser.new_context(**browser_context_args)

    context.add_cookies([{
        "name": "lang", "value": "ru-RU",
        "domain": "localhost", "path": "/"
    }])

    context.request.post(f"{os.getenv('BASE_URL_UI')}/user/login", form={
        "user_name": test_user_login,
        "password": test_user_pass,
    })

    page = context.new_page()

    yield page

    context.close()
    req.delete(f"{os.getenv('BASE_API_URL')}/admin/users/" + test_user_login,
               headers={"Authorization": f"token {os.getenv('ADMIN_TOKEN')}"},
               params='purge=true')

@pytest.fixture()
def register_page(page: Page):
    page.goto(f"{os.getenv('BASE_URL_UI')}/user/sign_up")
    yield
    req.delete(f"{os.getenv('BASE_API_URL')}/admin/users/" + TEST_LOGIN,
               headers={"Authorization": f"token {os.getenv("ADMIN_TOKEN")}"},
               params='purge=true')

@pytest.fixture()
def register_person_for_auth(page: Page):
    test_user_login = random_login()
    test_user_pass = random_password()
    test_user_email = random_email()

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