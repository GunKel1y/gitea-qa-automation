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

def create_repo(*, owner: str, repo_name: str) -> req.Response:
    return req.post(
        f"{BASE_URL_API}/admin/users/{owner}/repos",
        headers=HEADERS,
        json={"name": repo_name}
    )

def delete_repo(*, owner: str, repo_name: str) -> req.Response:
    return req.delete(
        f"{BASE_URL_API}/repos/{owner}/{repo_name}",
        headers=HEADERS
    )