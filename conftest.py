import os
import pytest

from pathlib import Path
from dotenv import load_dotenv

from playwright.sync_api import Page, Browser

from helpers.api_client import create_user, delete_user, create_repo, delete_repo, create_organization, \
    delete_organization, create_organization_by_user, create_user_token, create_team, add_team_member, \
    delete_issue_repo, create_issue_repo, create_milestone, create_label_issue, add_label_on_repo, \
    create_timeline_comment, delete_timeline_comment
from helpers.test_data import random_password, random_email, unique_name, get_random_color

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
    user = {"login": unique_name(prefix='user'), "password": random_password(), "email": random_email()}
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
    user = {"login": unique_name(prefix='user'), "password": random_password(), "email": random_email()}
    yield user
    delete_user(user["login"])

@pytest.fixture()
def created_public_repo(test_user):
    repo_name = unique_name(prefix='repo')
    create_repo(owner=test_user["login"], repo_name=repo_name, private=False)

    yield {"repo_name": repo_name}

    delete_repo(owner=test_user["login"], repo_name=repo_name)

@pytest.fixture()
def created_private_repo(test_user):
    repo_name = unique_name(prefix='repo')
    create_repo(owner=test_user["login"], repo_name=repo_name, private=True)

    yield {"repo_name": repo_name}

    delete_repo(owner=test_user["login"], repo_name=repo_name)

@pytest.fixture()
def created_public_organization_by_user(test_user):
    org_name = unique_name(prefix='org')

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
    org_name = unique_name(prefix='user')

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
    issue_name = unique_name(prefix='issue')
    issue_comment = unique_name(prefix='comment-issue')
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
    issue_name = unique_name(prefix='issue')
    issue_comment = unique_name(prefix='comment')
    create_issue_response = create_issue_repo(
        owner_repo=test_user["login"],
        repo_name=created_public_repo["repo_name"],
        title=issue_name,
        closed=False,
        comment=issue_comment
    )
    issue_index = create_issue_response.json()["number"]
    issue_id = create_issue_response.json()["id"]

    label_name = unique_name(prefix='label')
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

@pytest.fixture()
def created_label_on_issue(created_public_repo, test_user):
    label_name = unique_name(prefix='label')
    label_color = get_random_color()

    create_label_issue(
        owner_repo=test_user["login"],
        repo_name=created_public_repo["repo_name"],
        label_name=label_name,
        label_color=label_color
    )

    yield {"label_name": label_name}

@pytest.fixture()
def created_milestone(created_public_repo, test_user):
    milestone_name = unique_name(prefix='milestone')

    create_milestone(
        owner_repo=test_user["login"],
        repo_name=created_public_repo["repo_name"],
        milestone_name=milestone_name
    )

    yield {"milestone_name": milestone_name}

@pytest.fixture()
def created_timeline_comment(created_public_repo, test_user, created_repo_issue):
    comment = unique_name(prefix='comment')
    create_comment_response = create_timeline_comment(
        owner_repo=test_user["login"],
        repo_name=created_public_repo["repo_name"],
        issue_index=created_repo_issue["issue_index"],
        comment=comment
    )
    comment_id = create_comment_response.json()["id"]

    yield {"comment_id": comment_id, "comment_name": comment}

    delete_timeline_comment(
        owner_repo=test_user["login"],
        repo_name=created_public_repo["repo_name"],
        comment_id=comment_id
    )