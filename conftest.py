import os
import pytest

from pathlib import Path
from dotenv import load_dotenv

from playwright.sync_api import Page, Browser

from helpers.api_client import create_user, delete_user, create_repo, delete_repo, create_organization, \
    delete_organization, create_organization_by_user, create_user_token, create_team, add_team_member, \
    delete_issue_repo, create_issue_repo, create_label_issue, add_label_on_repo
from helpers.test_data import random_login, random_password, random_email, random_repo_name, get_random_color

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
    create_repo(owner=test_user["login"], repo_name=repo_name, private=False, issue_labels="Advanced")

    yield {"repo_name": repo_name}

    delete_repo(owner=test_user["login"], repo_name=repo_name)

@pytest.fixture()
def created_private_repo(test_user):
    repo_name = random_repo_name()
    create_repo(owner=test_user["login"], repo_name=repo_name, private=True, issue_labels="Advanced")

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

@pytest.fixture()
def created_organization_without_creation_rights(test_user):
    org_name = random_login()

    org_resp = create_organization(org_name=org_name, visibility="public")
    assert org_resp.ok, f"Ошибка создания организации: {org_resp.status_code} {org_resp.text}"

    team_resp = create_team(
        org_name=org_name,
        team_name="no-repo-create",
        permission="read",
        can_create_org_repo=False,
    )
    assert team_resp.ok, f"Ошибка создания команды: {team_resp.status_code} {team_resp.text}"
    team_id = team_resp.json()["id"]

    member_resp = add_team_member(team_id=team_id, username=test_user["login"])
    assert member_resp.ok, f"Ошибка добавления участника в команду: {member_resp.status_code} {member_resp.text}"

    yield {"name": org_name}

    delete_organization(org_name)

@pytest.fixture()
def created_repo_issue(created_public_repo, test_user):
    issue_name = random_login()
    issue_comment = random_login()
    create_issue_response = create_issue_repo(
        owner_repo=test_user["login"],
        repo_name=created_public_repo["repo_name"],
        title=issue_name,
        closed=False,
        comment=issue_comment
    )
    issue_index = create_issue_response.json()["number"]
    issue_id = create_issue_response.json()["id"]

    yield {"issue_id": issue_id, "issue_index": issue_index, "issue_name": issue_name}

    delete_issue_repo(
        owner_repo=test_user["login"],
        repo_name=created_public_repo["repo_name"],
        issue_index=issue_index
    )

@pytest.fixture()
def created_repo_issue_with_label(created_public_repo, test_user):
    issue_name = random_login()
    issue_comment = random_login()
    create_issue_response = create_issue_repo(
        owner_repo=test_user["login"],
        repo_name=created_public_repo["repo_name"],
        title=issue_name,
        closed=False,
        comment=issue_comment
    )
    issue_index = create_issue_response.json()["number"]
    issue_id = create_issue_response.json()["id"]

    label_name = random_login()
    label_color = get_random_color()
    create_label_issue(
        owner_repo=test_user["login"],
        repo_name=created_public_repo["repo_name"],
        label_name=label_name,
        label_color=label_color
    )
    add_label_on_repo(
        owner_repo=test_user["login"],
        repo_name=created_public_repo["repo_name"],
        issue_index=issue_index,
        labels=[label_name]
    )

    yield {"issue_id": issue_id, "issue_index": issue_index, "issue_name": issue_name, "label_name": label_name}

    delete_issue_repo(
        owner_repo=test_user["login"],
        repo_name=created_public_repo["repo_name"],
        issue_index=issue_index
    )