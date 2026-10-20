import os
from pathlib import Path

from dotenv import load_dotenv
import requests as req

load_dotenv(Path(__file__).parent.parent / ".env")

BASE_URL_API = os.getenv("GITEA_API_URL")
GITEA_ADMIN_TOKEN = os.getenv("GITEA_ADMIN_TOKEN")

API_TIMEOUT = (5, 15)
HEADERS = {"Authorization": f"token {GITEA_ADMIN_TOKEN}"}

def create_user(*, username: str, password: str, email: str, must_change_password: bool = False) -> req.Response:
    return req.post(
        f"{BASE_URL_API}/admin/users",
        headers=HEADERS,
        json={
            "username": username,
            "password": password,
            "email": email,
            "must_change_password": must_change_password
        },
        timeout=API_TIMEOUT
    )

def delete_user(username: str) -> req.Response:
    return req.delete(
        f"{BASE_URL_API}/admin/users/{username}",
        headers=HEADERS,
        params={"purge": "true"},
        timeout=API_TIMEOUT
    )

def create_repo(
        *,
        owner: str,
        repo_name: str,
        description: str = None,
        private: bool,
        auto_init: bool = False,
        gitignores_type: str = None,
        license_type: str = None,
        issue_labels: str = None,
        readme: str = "Default",
        is_template: bool = False,
) -> req.Response:
    return req.post(
        f"{BASE_URL_API}/admin/users/{owner}/repos",
        headers=HEADERS,
        json={
            "auto_init": auto_init,
            "name": repo_name,
            "description": description,
            "private": private,
            "readme": readme,
            "issue_labels": issue_labels,
            "gitignores": gitignores_type,
            "license": license_type,
            "template": is_template,
        },
        timeout=API_TIMEOUT
    )

def delete_repo(*, owner: str, repo_name: str) -> req.Response:
    return req.delete(
        f"{BASE_URL_API}/repos/{owner}/{repo_name}",
        headers=HEADERS,
        timeout=API_TIMEOUT
    )

def create_user_token(*, username: str, password: str, scopes: list[str], token_name: str = "test-token") -> req.Response:
    return req.post(
        f"{BASE_URL_API}/users/{username}/tokens",
        auth=(username, password),
        json={
            "name": token_name,
            "scopes": scopes
        },
        timeout=API_TIMEOUT
    )

def create_organization(*, org_name: str, visibility: str) -> req.Response:
    return req.post(
        f"{BASE_URL_API}/orgs",
        headers=HEADERS,
        json={
            "username": org_name,
            "visibility": visibility
        },
        timeout=API_TIMEOUT
    )

def delete_organization(org_name: str) -> req.Response:
    return req.delete(
        f"{BASE_URL_API}/orgs/{org_name}",
        headers=HEADERS,
        timeout=API_TIMEOUT
    )

def create_organization_by_user(*, org_name: str, visibility: str, user_token: str) -> req.Response:
    return req.post(
        f"{BASE_URL_API}/orgs",
        headers={"Authorization": f"token {user_token}"},
        json={
            "username": org_name,
            "visibility": visibility
        },
        timeout=API_TIMEOUT
    )

def create_team(*, org_name: str, team_name: str, permission: str, can_create_org_repo: bool,
                 units: list[str] | None = None) -> req.Response:
    return req.post(
        f"{BASE_URL_API}/orgs/{org_name}/teams",
        headers=HEADERS,
        json={
            "name": team_name,
            "permission": permission,
            "can_create_org_repo": can_create_org_repo,
            "units": units or ["repo.code"],
        },
        timeout=API_TIMEOUT
    )

def add_team_member(*, team_id: int, username: str) -> req.Response:
    return req.put(
        f"{BASE_URL_API}/teams/{team_id}/members/{username}",
        headers=HEADERS,
        timeout=API_TIMEOUT
    )

def create_issue_repo(*, owner_repo: str, repo_name: str, title: str, closed: bool, comment: str = None) -> req.Response:
    return req.post(
        f"{BASE_URL_API}/repos/{owner_repo}/{repo_name}/issues",
        headers=HEADERS,
        json={
            "title": title,
            "closed": closed,
            "body": comment
        },
        timeout=API_TIMEOUT
    )

def delete_issue_repo(*, owner_repo: str, repo_name: str, issue_index: int) -> req.Response:
    return req.delete(
        f"{BASE_URL_API}/repos/{owner_repo}/{repo_name}/issues/{issue_index}",
        headers=HEADERS,
        timeout=API_TIMEOUT
    )

def create_label_issue(*, owner_repo: str, repo_name: str, label_name: str, label_color: str) -> req.Response:
    return req.post(
        f"{BASE_URL_API}/repos/{owner_repo}/{repo_name}/labels",
        headers=HEADERS,
        json = {
            "name": label_name,
            "color": label_color
        },
        timeout=API_TIMEOUT
    )

def add_label_on_repo(*, owner_repo: str, repo_name: str, issue_index: int, labels: list[str]) -> req.Response:
    return req.post(
        f"{BASE_URL_API}/repos/{owner_repo}/{repo_name}/issues/{issue_index}/labels",
        headers=HEADERS,
        json={
            "labels": labels
        },
        timeout=API_TIMEOUT
    )

def create_milestone(*, owner_repo: str, repo_name: str, milestone_name: str) -> req.Response:
    return req.post(
        f"{BASE_URL_API}/repos/{owner_repo}/{repo_name}/milestones",
        headers=HEADERS,
        json={
            "title": milestone_name
        },
        timeout=API_TIMEOUT
    )

def create_timeline_comment(*, owner_repo: str, repo_name: str, issue_index: int, comment: str) -> req.Response:
    return req.post(
        f"{BASE_URL_API}/repos/{owner_repo}/{repo_name}/issues/{issue_index}/comments",
        headers = HEADERS,
        json = {
            "body": comment
        },
        timeout=API_TIMEOUT
    )

def delete_timeline_comment(*, owner_repo: str, repo_name: str, comment_id: int) -> req.Response:
    return req.delete(
        f"{BASE_URL_API}/repos/{owner_repo}/{repo_name}/issues/comments/{comment_id}",
        headers=HEADERS,
        timeout=API_TIMEOUT
    )

def update_repo_ability_repo_add_issues(*, owner_repo: str, repo_name: str, has_issues: bool) -> req.Response:
    return req.patch(
        f"{BASE_URL_API}/repos/{owner_repo}/{repo_name}",
        headers=HEADERS,
        json={
            "has_issues": has_issues
        },
        timeout=API_TIMEOUT
    )

def adding_collaborator_for_repo(
        *, owner_repo: str, repo_name: str, collaborator_login: str, permission: str
) -> req.Response:
    return req.put(
        f"{BASE_URL_API}/repos/{owner_repo}/{repo_name}/collaborators/{collaborator_login}",
        headers=HEADERS,
        json={
            "permission": permission
        },
        timeout=API_TIMEOUT
    )

def delete_collaborator_for_repo(*, owner_repo: str, repo_name: str, collaborator_login: str) -> req.Response:
    return req.delete(
        f"{BASE_URL_API}/repos/{owner_repo}/{repo_name}/collaborators/{collaborator_login}",
        headers=HEADERS,
        timeout=API_TIMEOUT
    )

def get_licenses() -> req.Response:
    licenses = req.get(
        f"{BASE_URL_API}/licenses",
        headers=HEADERS,
        timeout=API_TIMEOUT
    )
    assert licenses.ok, f"Ошибка при получении списка лицензий: {licenses.status_code} {licenses.text}"
    return licenses

def get_gitignore_templates() -> req.Response:
    gitignore_templates = req.get(
        f"{BASE_URL_API}/gitignore/templates",
        headers=HEADERS,
        timeout=API_TIMEOUT
    )
    assert gitignore_templates.ok,\
        f"Ошибка при получении списка gitignore: {gitignore_templates.status_code} {gitignore_templates.text}"
    return gitignore_templates