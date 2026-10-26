import os
from pathlib import Path

import requests as req
from dotenv import load_dotenv


load_dotenv(Path(__file__).parent.parent / ".env")

# ===========================================#
#             Настройка запросов            #
# ===========================================#

BASE_URL_API = os.getenv("GITEA_API_URL")
API_TIMEOUT = (5, 15)
_admin_token: str | None = None


def set_admin_token(token: str | None) -> None:
    """Вызывается только фикстурой admin_token"""
    global _admin_token
    _admin_token = token


def _headers() -> dict:
    """Хедеры админа для запросов"""
    if _admin_token is None:
        raise RuntimeError("Админ-токен не задан")
    return {"Authorization": f"token {_admin_token}"}


# ===========================================#
#                Пользователи               #
# ===========================================#
def create_user(*, username: str, password: str, email: str, must_change_password: bool = False) -> req.Response:
    """Создает пользователя на стенде через админа"""
    return req.post(
        f"{BASE_URL_API}/admin/users",
        headers=_headers(),
        json={"username": username, "password": password, "email": email, "must_change_password": must_change_password},
        timeout=API_TIMEOUT,
    )


def delete_user(username: str) -> req.Response:
    """Удаляет пользователя на стенде через админа"""
    return req.delete(
        f"{BASE_URL_API}/admin/users/{username}", headers=_headers(), params={"purge": "true"}, timeout=API_TIMEOUT
    )


def create_user_token(
    *, username: str, password: str, scopes: list[str], token_name: str = "test-token"
) -> req.Response:
    """Создает токен пользователя с правами (scopes)"""
    return req.post(
        f"{BASE_URL_API}/users/{username}/tokens",
        auth=(username, password),
        json={"name": token_name, "scopes": scopes},
        timeout=API_TIMEOUT,
    )


# ===========================================#
#                 Репозитории               #
# ===========================================#


def create_repo(
    *,
    owner: str,
    repo_name: str,
    description: str | None = None,
    private: bool,
    auto_init: bool = False,
    gitignores_type: str | None = None,
    license_type: str | None = None,
    issue_labels: str | None = None,
    readme: str = "Default",
    is_template: bool = False,
) -> req.Response:
    """Создает репозиторий на стенде через админа"""
    return req.post(
        f"{BASE_URL_API}/admin/users/{owner}/repos",
        headers=_headers(),
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
        timeout=API_TIMEOUT,
    )


def delete_repo(*, owner: str, repo_name: str) -> req.Response:
    """Удаляет репозиторий на стенде через админа"""
    return req.delete(f"{BASE_URL_API}/repos/{owner}/{repo_name}", headers=_headers(), timeout=API_TIMEOUT)


def update_repo_ability_repo_add_issues(*, owner_repo: str, repo_name: str, has_issues: bool) -> req.Response:
    """Изменяет возможность добавления задач в репозитории через админа"""
    return req.patch(
        f"{BASE_URL_API}/repos/{owner_repo}/{repo_name}",
        headers=_headers(),
        json={"has_issues": has_issues},
        timeout=API_TIMEOUT,
    )


def adding_collaborator_for_repo(
    *, owner_repo: str, repo_name: str, collaborator_login: str, permission: str
) -> req.Response:
    """Добавляет соавтора в репозиторий с правами (read/write/admin)"""
    return req.put(
        f"{BASE_URL_API}/repos/{owner_repo}/{repo_name}/collaborators/{collaborator_login}",
        headers=_headers(),
        json={"permission": permission},
        timeout=API_TIMEOUT,
    )


def delete_collaborator_for_repo(*, owner_repo: str, repo_name: str, collaborator_login: str) -> req.Response:
    """Удаляет соавтора в репозитории"""
    return req.delete(
        f"{BASE_URL_API}/repos/{owner_repo}/{repo_name}/collaborators/{collaborator_login}",
        headers=_headers(),
        timeout=API_TIMEOUT,
    )


# ===========================================#
#                 Организации               #
# ===========================================#


def create_organization(*, org_name: str, visibility: str) -> req.Response:
    """Создает организацию через админа со значением видимости (public/limited/private)"""
    return req.post(
        f"{BASE_URL_API}/orgs",
        headers=_headers(),
        json={"username": org_name, "visibility": visibility},
        timeout=API_TIMEOUT,
    )


def delete_organization(org_name: str) -> req.Response:
    """Удаляет организацию через админа"""
    return req.delete(f"{BASE_URL_API}/orgs/{org_name}", headers=_headers(), timeout=API_TIMEOUT)


def create_organization_by_user(*, org_name: str, visibility: str, user_token: str) -> req.Response:
    """Создает организацию через токен юзера"""
    return req.post(
        f"{BASE_URL_API}/orgs",
        headers={"Authorization": f"token {user_token}"},
        json={"username": org_name, "visibility": visibility},
        timeout=API_TIMEOUT,
    )


def create_team(
    *, org_name: str, team_name: str, permission: str, can_create_org_repo: bool, units: list[str] | None = None
) -> req.Response:
    """Создает команду с правами (permission) и возможностью добавления репозиториев (can_create_org_repo)"""
    return req.post(
        f"{BASE_URL_API}/orgs/{org_name}/teams",
        headers=_headers(),
        json={
            "name": team_name,
            "permission": permission,
            "can_create_org_repo": can_create_org_repo,
            "units": units or ["repo.code"],
        },
        timeout=API_TIMEOUT,
    )


def add_team_member(*, team_id: int, username: str) -> req.Response:
    """Добавляет юзера в команду через админа"""
    return req.put(f"{BASE_URL_API}/teams/{team_id}/members/{username}", headers=_headers(), timeout=API_TIMEOUT)


# ==========================================#
#                  Задачи                  #
# ==========================================#


def create_issue_repo(
    *, owner_repo: str, repo_name: str, title: str, closed: bool, comment: str | None = None
) -> req.Response:
    """Создает задачу в репозитории через админа"""
    return req.post(
        f"{BASE_URL_API}/repos/{owner_repo}/{repo_name}/issues",
        headers=_headers(),
        json={"title": title, "closed": closed, "body": comment},
        timeout=API_TIMEOUT,
    )


def delete_issue_repo(*, owner_repo: str, repo_name: str, issue_index: int) -> req.Response:
    """Удаляет задачу в репозитории через админа"""
    return req.delete(
        f"{BASE_URL_API}/repos/{owner_repo}/{repo_name}/issues/{issue_index}", headers=_headers(), timeout=API_TIMEOUT
    )


def create_label_issue(*, owner_repo: str, repo_name: str, label_name: str, label_color: str) -> req.Response:
    """Создает метку для задач в репозитории через админа"""
    return req.post(
        f"{BASE_URL_API}/repos/{owner_repo}/{repo_name}/labels",
        headers=_headers(),
        json={"name": label_name, "color": label_color},
        timeout=API_TIMEOUT,
    )


def add_label_on_repo(*, owner_repo: str, repo_name: str, issue_index: int, labels: list[str]) -> req.Response:
    """Добавляет метку задаче из репозитория через админа"""
    return req.post(
        f"{BASE_URL_API}/repos/{owner_repo}/{repo_name}/issues/{issue_index}/labels",
        headers=_headers(),
        json={"labels": labels},
        timeout=API_TIMEOUT,
    )


def create_milestone(*, owner_repo: str, repo_name: str, milestone_name: str) -> req.Response:
    """Добавляет этап в репозитории через админа"""
    return req.post(
        f"{BASE_URL_API}/repos/{owner_repo}/{repo_name}/milestones",
        headers=_headers(),
        json={"title": milestone_name},
        timeout=API_TIMEOUT,
    )


def create_timeline_comment(*, owner_repo: str, repo_name: str, issue_index: int, comment: str) -> req.Response:
    """Добавляет комментарий в ленте событий задачи"""
    return req.post(
        f"{BASE_URL_API}/repos/{owner_repo}/{repo_name}/issues/{issue_index}/comments",
        headers=_headers(),
        json={"body": comment},
        timeout=API_TIMEOUT,
    )


def delete_timeline_comment(*, owner_repo: str, repo_name: str, comment_id: int) -> req.Response:
    """Удаляет комментарий из ленты событий задачи"""
    return req.delete(
        f"{BASE_URL_API}/repos/{owner_repo}/{repo_name}/issues/comments/{comment_id}",
        headers=_headers(),
        timeout=API_TIMEOUT,
    )


# =========================================#
#               Справочники               #
# =========================================#


def get_licenses() -> req.Response:
    """Возвращает ответ со списком лицензий стенда"""
    licenses = req.get(f"{BASE_URL_API}/licenses", headers=_headers(), timeout=API_TIMEOUT)
    assert licenses.ok, f"Ошибка при получении списка лицензий: {licenses.status_code} {licenses.text}"
    return licenses


def get_gitignore_templates() -> req.Response:
    """Возвращает ответ со списком gitignore значений стенда"""
    gitignore_templates = req.get(f"{BASE_URL_API}/gitignore/templates", headers=_headers(), timeout=API_TIMEOUT)
    assert gitignore_templates.ok, (
        f"Ошибка при получении списка gitignore: {gitignore_templates.status_code} {gitignore_templates.text}"
    )
    return gitignore_templates
