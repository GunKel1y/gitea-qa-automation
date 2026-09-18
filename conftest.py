from uuid import uuid4

from playwright.sync_api import Page, expect
import pytest
import requests as req

TEST_LOGIN = 'test_username-' + str(uuid4())[:20]

@pytest.fixture()
def register_page(page: Page):
    page.goto("http://localhost:3000/user/sign_up")
    yield
    req.delete("http://localhost:3000/api/v1/admin/users/" + TEST_LOGIN, params='purge=true')
