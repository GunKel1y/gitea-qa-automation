import os
from pathlib import Path

from dotenv import load_dotenv
import requests as req

load_dotenv(Path(__file__).parent.parent / ".env")

BASE_URL_API = os.getenv("BASE_API_URL")
ADMIN_TOKEN = os.getenv("ADMIN_TOKEN")

HEADERS = {"Authorization": f"token {ADMIN_TOKEN}"}

def create_user(*, username: str, password: str, email: str, must_change_password: bool = False) -> req.Response:
    return req.post(
        f"{BASE_URL_API}/admin/users",
        headers=HEADERS,
        json={
            "username": username,
            "password": password,
            "email": email,
            "must_change_password": must_change_password
        }
    )

def delete_user(username: str) -> req.Response:
    return req.delete(
        f"{BASE_URL_API}/admin/users/{username}",
        headers=HEADERS,
        params={"purge": "true"}
    )

def create_repo(*, owner: str, repo_name: str, private: bool, issue_labels: str = None) -> req.Response:
    return req.post(
        f"{BASE_URL_API}/admin/users/{owner}/repos",
        headers=HEADERS,
        json={"name": repo_name, "private": private, "issue_labels": issue_labels}
    )

def delete_repo(*, owner: str, repo_name: str) -> req.Response:
    return req.delete(
        f"{BASE_URL_API}/repos/{owner}/{repo_name}",
        headers=HEADERS
    )

def create_user_token(*, username: str, password: str, scopes: list[str], token_name: str = "test-token") -> req.Response:
    return req.post(
        f"{BASE_URL_API}/users/{username}/tokens",
        auth=(username, password),
        json={
            "name": token_name,
            "scopes": scopes
        }
    )

def create_organization(*, org_name: str, visibility: str) -> req.Response:
    return req.post(
        f"{BASE_URL_API}/orgs",
        headers=HEADERS,
        json={
            "username": org_name,
            "visibility": visibility
        }
    )

def delete_organization(org_name: str) -> req.Response:
    return req.delete(
        f"{BASE_URL_API}/orgs/{org_name}",
        headers=HEADERS
    )

def create_organization_by_user(*, org_name: str, visibility: str, user_token: str) -> req.Response:
    return req.post(
        f"{BASE_URL_API}/orgs",
        headers={"Authorization": f"token {user_token}"},
        json={
            "username": org_name,
            "visibility": visibility
        }
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
        }
    )

def add_team_member(*, team_id: int, username: str) -> req.Response:
    return req.put(
        f"{BASE_URL_API}/teams/{team_id}/members/{username}",
        headers=HEADERS
    )

def create_issue_repo(*, owner_repo: str, repo_name: str, title: str, closed: bool, comment: str) -> req.Response:
    return req.post(
        f"{BASE_URL_API}/repos/{owner_repo}/{repo_name}/issues",
        headers=HEADERS,
        json={
            "title": title,
            "closed": closed,
            "body": comment
        }
    )

def delete_issue_repo(*, owner_repo: str, repo_name: str, issue_index: int):
    return req.delete(
        f"{BASE_URL_API}/repos/{owner_repo}/{repo_name}/issues/{issue_index}",
        headers=HEADERS
    )

def create_label_issue(*, owner_repo: str, repo_name: str, label_name: str, label_color: str):
    return req.post(
        f"{BASE_URL_API}/repos/{owner_repo}/{repo_name}/labels",
        headers=HEADERS,
        json = {
            "name": label_name,
            "color": label_color
        }
    )

def add_label_on_repo(*, owner_repo: str, repo_name: str, issue_index: int, labels: list[str]):
    return req.post(
        f"{BASE_URL_API}/repos/{owner_repo}/{repo_name}/issues/{issue_index}/labels",
        headers=HEADERS,
        json={
            "labels": labels
        }
    )

def create_milestone(*, owner_repo: str, repo_name: str, milestone_name: str):
    return req.post(
        f"{BASE_URL_API}/repos/{owner_repo}/{repo_name}/milestones",
        headers=HEADERS,
        json={
            "title": milestone_name
        }
    )

def create_timeline_comment(*, owner_repo: str, repo_name: str, issue_index: int, comment: str):
    return req.post(
        f"{BASE_URL_API}/repos/{owner_repo}/{repo_name}/issues/{issue_index}/comments",
        headers = HEADERS,
        json = {
            "body": comment
        }
    )

def delete_timeline_comment(*, owner_repo: str, repo_name: str, comment_id: int):
    return req.post(
        f"{BASE_URL_API}/repos/{owner_repo}/{repo_name}/issues/comments/{comment_id}",
        headers=HEADERS
    )