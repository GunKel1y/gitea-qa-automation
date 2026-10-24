import os
import random
from uuid import uuid4

import pytest

from pathlib import Path

import requests
from dotenv import load_dotenv

from playwright.sync_api import Browser

from helpers.api_client import create_user, delete_user, create_repo, delete_repo, create_organization, \
    delete_organization, create_organization_by_user, create_user_token, create_team, add_team_member, \
    delete_issue_repo, create_issue_repo, create_milestone, create_label_issue, add_label_on_repo, \
    create_timeline_comment, delete_timeline_comment, update_repo_ability_repo_add_issues, adding_collaborator_for_repo, \
    delete_collaborator_for_repo, get_licenses, get_gitignore_templates, set_admin_token
from helpers.test_data import random_password, random_email, unique_name, get_random_color

load_dotenv(Path(__file__).parent / ".env")

#===========================================#
#       Приватные хелперы для фикстур       #
#===========================================#

def _login_context(*, browser, browser_context_args, user):
    """Возвращает контекст браузера, авторизованный через API запрос (без UI), с русскими куками"""
    context = browser.new_context(**browser_context_args)
    context.add_cookies([{"name": "lang", "value": "ru-RU", "url": os.getenv("GITEA_UI_URL")}])
    authorized = context.request.post(f"{os.getenv('GITEA_UI_URL')}/user/login", form={
        "user_name": user["login"],
        "password": user["password"],
    })
    assert authorized.ok and "/user/login" not in authorized.url, f"Ошибка входа: {authorized.status} {authorized.url}"
    return context

def _make_user() -> dict:
    """Создает нового пользователя со случайными данными, возвращает его login, password и email словарем"""
    user = {"login": unique_name(prefix='user'), "password": random_password(), "email": random_email()}
    created_user = create_user(username=user["login"], email=user["email"], password=user["password"])
    assert created_user.ok, f"Ошибка при создании пользователя: {created_user.status_code} {created_user.text}"
    return user

#===========================================#
#            Сессионные фикстуры            #
#===========================================#
@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Опции контекста браузера: размер окна и русский язык интерфейса"""
    return {**browser_context_args,
            "viewport": {"width": 1920, "height": 1080},
            "locale": "ru-RU"
            }

@pytest.fixture(scope="session", autouse=True)
def admin_token(worker_id):
    """Создает токен админа, отдает в api_client и удаляет в конце тестовой сессии"""
    API_URL = os.getenv("GITEA_API_URL")
    ADMIN_LOGIN = os.getenv("GITEA_ADMIN_LOGIN")
    ADMIN_PASS = os.getenv("GITEA_ADMIN_PASSWORD")
    name = f"tests-{worker_id}-{uuid4().hex[:8]}"

    tokens_response = requests.post(
        f"{API_URL}/users/{ADMIN_LOGIN}/tokens",
        auth=(ADMIN_LOGIN, ADMIN_PASS),
        json={"name": name, "scopes": ["all"]},
    )
    assert tokens_response.status_code == 201,\
        f"Ошибка создания админ-токена: {tokens_response.status_code} {tokens_response.text}"

    token = tokens_response.json()["sha1"]
    set_admin_token(token)

    yield token

    set_admin_token(None)
    requests.delete(
        f"{API_URL}/users/{ADMIN_LOGIN}/tokens/{name}",
        auth=(ADMIN_LOGIN, ADMIN_PASS),
    )

#===========================================#
#            Авторизация и юзеры            #
#===========================================#

@pytest.fixture()
def test_user():
    """Создает пользователя со случайными данными, после теста удаляет его"""
    user = _make_user()
    yield {"login": user["login"], "password": user["password"], "email": user["email"]}
    delete_user(user["login"])

@pytest.fixture()
def second_test_user():
    """Создает второго пользователя для сценариев с двумя участниками"""
    user = _make_user()
    yield {"login": user["login"], "password": user["password"], "email": user["email"]}
    delete_user(user["login"])

@pytest.fixture()
def authenticated_user_page(browser: Browser, browser_context_args, test_user):
    """Авторизованная страница браузера под test_user, контекст закрывается после теста"""
    context = _login_context(browser=browser, browser_context_args=browser_context_args, user=test_user)
    yield context.new_page()
    context.close()

@pytest.fixture()
def authenticated_second_user_page(browser: Browser, browser_context_args, second_test_user):
    """Авторизованная страница браузера под second_test_user, в отдельном контексте от первого юзера"""
    context = _login_context(browser=browser, browser_context_args=browser_context_args, user=second_test_user)
    yield context.new_page()
    context.close()

@pytest.fixture()
def delete_user_after_registration(request):
    """
    Готовит данные пользователя для теста регистрации (из param или случайные) и удаляет его после теста
    Сам пользователь не создается, фикстура только чистит за тестом
    """
    if getattr(request, "param", None):
        login, password, email = request.param
    else:
        login, password, email = unique_name(prefix='user'), random_password(), random_email()

    user = {"login": login, "password": password, "email": email}
    yield user
    delete_user(user["login"])

#===========================================#
#                Репозитории                #
#===========================================#

@pytest.fixture()
def created_public_repo(test_user):
    """Создает публичный репозиторий, после теста удаляет"""
    repo_name = unique_name(prefix='repo')
    created_repo = create_repo(owner=test_user["login"], repo_name=repo_name, private=False)
    assert created_repo.ok, f"Ошибка создания публичного репозитория: {created_repo.status_code} {created_repo.text}"

    yield {"repo_name": repo_name}

    delete_repo(owner=test_user["login"], repo_name=repo_name)

@pytest.fixture()
def created_private_repo(test_user):
    """Создает приватный репозиторий, после теста удаляет"""
    repo_name = unique_name(prefix='repo')
    created_repo = create_repo(owner=test_user["login"], repo_name=repo_name, private=True)
    assert created_repo.ok, f"Ошибка создания приватного репозитория: {created_repo.status_code} {created_repo.text}"

    yield {"repo_name": repo_name}

    delete_repo(owner=test_user["login"], repo_name=repo_name)

@pytest.fixture()
def created_template_repo(test_user):
    """
    Создает публичный репозиторий-шаблон со случайными описанием, лицензией и .gitignore;

    Возвращает id, имя и выбранные параметры, чтобы тест мог сверить с ними
    репозиторий, созданный из шаблона;

    После теста репозиторий удаляется;
    """
    repo_owner = test_user["login"]
    repo_name = unique_name(prefix='repo')
    description = unique_name(prefix="description")
    license_type = random.choice(get_licenses().json())["name"]
    gitignore_type = random.choice(get_gitignore_templates().json())
    created_repo = create_repo(
        auto_init=True,
        owner=repo_owner,
        repo_name=repo_name,
        description=description,
        gitignores_type=gitignore_type,
        license_type=license_type,
        private=False,
        is_template=True
    )
    assert created_repo.ok, f"Ошибка создания репозитория-шаблона: {created_repo.status_code} {created_repo.text}"

    yield {
        "repo_id": created_repo.json()["id"],
        "repo_name": repo_name,
        "description": description,
        "license_type": license_type,
        "gitignore_type": gitignore_type
    }

    delete_repo(owner=repo_owner, repo_name=repo_name)

@pytest.fixture()
def created_template_repo_with_label(test_user):
    """
    Создает репозиторий-шаблон с двумя случайными метками, возвращает id, имя и названия меток;

    Репозиторий удаляется после теста
    """
    repo_owner = test_user["login"]
    repo_name = unique_name(prefix='repo')

    created_repo = create_repo(
        auto_init=True,
        owner=repo_owner,
        repo_name=repo_name,
        private=False,
        is_template=True
    )
    assert created_repo.ok, f"Ошибка создания репозитория-шаблона: {created_repo.status_code} {created_repo.text}"

    try:
        created_labels = []

        for _ in range(2):
            create_label_to_repo = create_label_issue(
                owner_repo=repo_owner,
                repo_name=repo_name,
                label_name=unique_name(prefix="label"),
                label_color=get_random_color()
            )
            assert create_label_to_repo.ok, \
                f"Ошибка создания метки в репозитории: {create_label_to_repo.status_code, create_label_to_repo.text}"

            created_labels.append(create_label_to_repo.json()["name"])

        yield {
            "repo_id": created_repo.json()["id"],
            "repo_name": repo_name,
            "labels": created_labels,
        }
    finally:
        delete_repo(owner=repo_owner, repo_name=repo_name)

@pytest.fixture()
def adding_collaboration_for_repo_with_admin_permission(created_public_repo, test_user, second_test_user):
    """Добавляет second_test_user соавтором с правами admin'а в публичный репозиторий, возвращает логин соавтора"""
    collaboration_name = second_test_user["login"]
    added_collaborator = adding_collaborator_for_repo(
        owner_repo=test_user["login"],
        repo_name=created_public_repo["repo_name"],
        collaborator_login=collaboration_name,
        permission="admin"
    )
    assert added_collaborator.ok, \
        f"Ошибка при добавлении соавтора репозитория: {added_collaborator.status_code} {added_collaborator.text}"

    yield {"collaborator_login": collaboration_name}

    delete_collaborator_for_repo(
        owner_repo=test_user["login"],
        repo_name=created_public_repo["repo_name"],
        collaborator_login=collaboration_name
    )

@pytest.fixture()
def disabling_ability_add_issue_to_repo(created_public_repo, test_user):
    """Отключает в публичном репозитории возможность создавать задачи"""
    updated_ability_add_issues = update_repo_ability_repo_add_issues(
        owner_repo=test_user["login"],
        repo_name=created_public_repo["repo_name"],
        has_issues=False
    )
    assert updated_ability_add_issues.ok, \
        (f"Ошибка при отключении возможности добавлять задачи в репозитории: "
         f"{updated_ability_add_issues.status_code} {updated_ability_add_issues.text}")

@pytest.fixture()
def created_repo_label(created_public_repo, test_user):
    """Создает метку со случайным именем и цветом в публичном репозитории, возвращает имя метки"""
    label_name = unique_name(prefix='label')
    label_color = get_random_color()

    created_label = create_label_issue(
        owner_repo=test_user["login"],
        repo_name=created_public_repo["repo_name"],
        label_name=label_name,
        label_color=label_color
    )
    assert created_label.ok, f"Ошибка при создании метки: {created_label.status_code} {created_label.text}"

    yield {"label_name": label_name}

@pytest.fixture()
def created_milestone(created_public_repo, test_user):
    """Создает этап со случайным именем в публичном репозитории, возвращает его имя"""
    milestone_name = unique_name(prefix='milestone')

    created_milestone_resp = create_milestone(
        owner_repo=test_user["login"],
        repo_name=created_public_repo["repo_name"],
        milestone_name=milestone_name
    )
    assert created_milestone_resp.ok,\
        f"Ошибка при создании этапа: {created_milestone_resp.status_code} {created_milestone_resp.text}"

    yield {"milestone_name": milestone_name}

#===========================================#
#                Огранизации                #
#===========================================#

@pytest.fixture()
def created_public_organization_by_user(test_user):
    """Создает публичную организацию, после теста удаляет ее"""
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
    """Создает публичную организацию, где test_user состоит в команде только с правом чтения
    и без права создавать репозитории, после теста организация удаляется"""
    org_name = unique_name(prefix='org')

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

#===========================================#
#                   Задачи                  #
#===========================================#

@pytest.fixture()
def created_repo_issue(created_public_repo, test_user):
    """
    Создает задачу с закрепленным комментарием в публичном репозитории

    Возвращает id, номер, заголовок и текст комментария, после теста задача удаляется
    """
    issue_name = unique_name(prefix='issue')
    issue_comment = unique_name(prefix='comment-issue')
    created_issue = create_issue_repo(
        owner_repo=test_user["login"],
        repo_name=created_public_repo["repo_name"],
        title=issue_name,
        closed=False,
        comment=issue_comment
    )
    assert created_issue.ok, f"Ошибка при создании задачи: {created_issue.status_code} {created_issue.text}"
    issue_index = created_issue.json()["number"]
    issue_id = created_issue.json()["id"]

    yield {"issue_id": issue_id, "issue_index": issue_index, "issue_name": issue_name, "issue_comment": issue_comment}

    delete_issue_repo(
        owner_repo=test_user["login"],
        repo_name=created_public_repo["repo_name"],
        issue_index=issue_index
    )

@pytest.fixture()
def created_repo_issue_with_label(created_public_repo, test_user):
    """
    Создает задачу и новую метку в публичном репозитории, назначает метку задаче;

    Возвращает id, номер и заголовок задачи, имя метки. После теста задача удаляется
    """
    issue_name = unique_name(prefix='issue')
    issue_comment = unique_name(prefix='comment')
    created_issue = create_issue_repo(
        owner_repo=test_user["login"],
        repo_name=created_public_repo["repo_name"],
        title=issue_name,
        closed=False,
        comment=issue_comment
    )
    assert created_issue.ok, f"Ошибка при создании задачи: {created_issue.status_code} {created_issue.text}"
    issue_index = created_issue.json()["number"]
    issue_id = created_issue.json()["id"]

    label_name = unique_name(prefix='label')
    label_color = get_random_color()
    created_label = create_label_issue(
        owner_repo=test_user["login"],
        repo_name=created_public_repo["repo_name"],
        label_name=label_name,
        label_color=label_color
    )
    assert created_label.ok, f"Ошибка при создании метки: {created_label.status_code} {created_label.text}"

    added_label_for_issue = add_label_on_repo(
        owner_repo=test_user["login"],
        repo_name=created_public_repo["repo_name"],
        issue_index=issue_index,
        labels=[label_name]
    )
    assert added_label_for_issue.ok, \
        f"Ошибка при добавлении метки к задаче: {added_label_for_issue.status_code} {added_label_for_issue.text}"

    yield {"issue_id": issue_id, "issue_index": issue_index, "issue_name": issue_name, "label_name": label_name}

    delete_issue_repo(
        owner_repo=test_user["login"],
        repo_name=created_public_repo["repo_name"],
        issue_index=issue_index
    )

@pytest.fixture()
def created_closed_repo_issue(test_user, created_public_repo):
    """Создает закрытую задачу в публичном репозитории, возвращает ее номер, после теста задача удаляется"""
    issue_name = unique_name(prefix='issue')
    created_issue = create_issue_repo(
        owner_repo=test_user["login"],
        repo_name=created_public_repo["repo_name"],
        title=issue_name,
        closed=True
    )
    assert created_issue.ok, f"Ошибка при создании задачи: {created_issue.status_code} {created_issue.text}"
    issue_index = created_issue.json()["number"]

    yield {"issue_index": issue_index}

    delete_issue_repo(
        owner_repo=test_user["login"],
        repo_name=created_public_repo["repo_name"],
        issue_index=issue_index
    )

@pytest.fixture()
def created_timeline_comment(created_public_repo, test_user, created_repo_issue):
    """Добавляет комментарий в ленту задачи, возвращает id и текст комментария, после теста комментарий удаляется"""
    comment = unique_name(prefix='comment')
    created_comment = create_timeline_comment(
        owner_repo=test_user["login"],
        repo_name=created_public_repo["repo_name"],
        issue_index=created_repo_issue["issue_index"],
        comment=comment
    )
    assert created_comment.ok, f"Ошибка при создании комментария: {created_comment.status_code} {created_comment.text}"
    comment_id = created_comment.json()["id"]

    yield {"comment_id": comment_id, "comment_name": comment}

    delete_timeline_comment(
        owner_repo=test_user["login"],
        repo_name=created_public_repo["repo_name"],
        comment_id=comment_id
    )