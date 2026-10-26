import allure
import pytest
from playwright.sync_api import Page

from helpers.test_data import unique_name, value_with_length
from pages.dashboard_page import DashboardPage
from pages.not_found_error_page import NotFoundErrorPage
from pages.repo.create_repository_page import CreateRepositoryPage
from pages.repo.repo_issues_page import RepoIssuesPage
from pages.repo.repo_page import RepoPage


pytestmark = allure.epic("Репозитории")


@pytest.mark.parametrize(
    "repo_name, expected_name, title",
    [
        pytest.param(
            "a", "a", "Имя минимальной длины (1 символ)", id="min", marks=[pytest.mark.p3, allure.testcase("TC-R-030")]
        ),
        pytest.param(
            "a" * 100,
            "a" * 100,
            "Имя на границе максимальной длины (100 символов)",
            id="max",
            marks=[pytest.mark.p3, allure.testcase("TC-R-031")],
        ),
        pytest.param(
            "a" * 101,
            "a" * 100,
            "Имя длиннее максимума (101 символ) обрезается до 100",
            id="over_max_truncated",
            marks=[pytest.mark.p3, allure.testcase("TC-R-032")],
        ),
        pytest.param(
            "a b",
            "a-b",
            "Имя с пробелом: пробел заменяется на дефис",
            id="with_space",
            marks=[pytest.mark.p3, allure.testcase("TC-R-033")],
        ),
        pytest.param(
            "a/b",
            "a-b",
            "Имя со слэшем: слэш заменяется на дефис",
            id="with_slash",
            marks=[pytest.mark.p3, allure.testcase("TC-R-034")],
        ),
        pytest.param(
            "test-⭐",
            "test--",
            "Эмодзи внутри имени заменяется дефисом",
            id="emoji",
            marks=[pytest.mark.p2, allure.testcase("TC-R-023a")],
        ),
    ],
)
def test_name_validation(authenticated_user_page: Page, test_user, repo_name, expected_name, title):
    create_repo_page = CreateRepositoryPage(authenticated_user_page)
    repo_page = RepoPage(authenticated_user_page)

    with allure.step("Создать репозиторий с проверяемым названием"):
        create_repo_page.open()
        create_repo_page.fill_repo_name_field(repo_name)
        create_repo_page.click_repo_create_button()

    with allure.step("Проверить, что репозиторий создан"):
        repo_page.check_url(f"/{test_user['login']}/{expected_name}")
        repo_page.repo_header.repo_name_in_header_is_displayed(username=test_user["login"], repo_name=expected_name)


@allure.testcase("TC-R-035")
@allure.title("Репозиторий без readme/gitignore/license — пустой")
@allure.severity(allure.severity_level.MINOR)
@pytest.mark.p3
def test_create_repo_without_init_is_empty(authenticated_user_page: Page, test_user):
    create_repo_page = CreateRepositoryPage(authenticated_user_page)
    repo_page = RepoPage(authenticated_user_page)
    repo_name = unique_name(prefix="repo")

    with allure.step("Создать репозиторий без инициализации"):
        create_repo_page.open()
        create_repo_page.fill_repo_name_field(repo_name)
        create_repo_page.click_repo_create_button()

    with allure.step("Проверить, что репозиторий пустой"):
        repo_page.check_url(f"/{test_user['login']}/{repo_name}")
        repo_page.empty_repo_guide_is_displayed()


@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.p2
@pytest.mark.parametrize(
    "input_name, title",
    [
        pytest.param("", "Создание репозитория с пустым именем", id="empty_name", marks=allure.testcase("TC-R-020")),
        pytest.param(
            "..",
            "Создание репозитория с двумя точками в имени",
            id="with_double_dot",
            marks=allure.testcase("TC-R-022"),
        ),
        pytest.param("⭐", "Имя только из эмодзи отклоняется", id="emoji", marks=allure.testcase("TC-R-023b")),
    ],
)
@allure.title("{title}")
def test_name_validation_no_repo_create(authenticated_user_page: Page, input_name, title):
    create_repo_page = CreateRepositoryPage(authenticated_user_page)

    with allure.step("Открыть форму создания репозитория"):
        create_repo_page.open()
        create_repo_page.check_url("/repo/create")

    with allure.step("Попытаться создать репозиторий с невалидным названием"):
        create_repo_page.fill_repo_name_field(input_name)

        create_repo_page.click_repo_create_button()

    with allure.step("Проверить, что репозиторий не создан"):
        create_repo_page.check_url("/repo/create")
        create_repo_page.create_repo_form_is_displayed()


@allure.testcase("TC-R-021")
@allure.title("Создание репозитория с именем, которое уже существует у owner")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.p2
def test_create_repo_with_duplicate_name(authenticated_user_page: Page, created_public_repo):
    dashboard_page = DashboardPage(authenticated_user_page)
    create_repo_page = CreateRepositoryPage(authenticated_user_page)

    with allure.step("Открыть форму создания репозитория через меню"):
        dashboard_page.open()
        dashboard_page.global_header.click_dropdown_button()
        dashboard_page.global_header.click_create_new_repository_button()
        create_repo_page.check_url("/repo/create")

    with allure.step("Попытаться создать репозиторий с занятым названием"):
        create_repo_page.fill_repo_name_field(created_public_repo["repo_name"])

        create_repo_page.click_repo_create_button()

    with allure.step("Проверить сообщение об ошибке"):
        create_repo_page.error_message_has_text("Название репозитория уже используется.")


@allure.testcase("TC-R-001")
@allure.title("Создание репозитория с минимальным набором данных")
@allure.severity(allure.severity_level.BLOCKER)
@pytest.mark.p0
def test_create_public_repo(authenticated_user_page: Page, test_user):
    create_repo_page = CreateRepositoryPage(authenticated_user_page)
    repo_page = RepoPage(authenticated_user_page)
    repo_name = unique_name(prefix="repo")

    with allure.step("Создать публичный репозиторий"):
        create_repo_page.open()

        create_repo_page.fill_repo_name_field(repo_name)

        create_repo_page.click_repo_create_button()
    with allure.step("Проверить, что репозиторий создан"):
        repo_page.repo_header.repo_name_in_header_is_displayed(repo_name=repo_name, username=test_user["login"])
        repo_page.check_url(f"/{test_user['login']}/{repo_name}")


@allure.testcase("TC-R-011")
@allure.title("Создание приватного репозитория")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.p1
def test_create_private_repo(authenticated_user_page: Page, test_user):
    create_repo_page = CreateRepositoryPage(authenticated_user_page)
    repo_page = RepoPage(authenticated_user_page)
    repo_name = unique_name(prefix="repo")

    with allure.step("Создать приватный репозиторий"):
        create_repo_page.open()

        create_repo_page.fill_repo_name_field(repo_name)

        create_repo_page.select_checkbox_private_repo()

        create_repo_page.click_repo_create_button()
    with allure.step("Проверить, что репозиторий создан и приватный"):
        repo_page.repo_header.repo_name_in_header_is_displayed(repo_name=repo_name, username=test_user["login"])
        repo_page.check_url(f"/{test_user['login']}/{repo_name}")

        repo_page.privacy_status_is_displayed()


@allure.testcase("TC-R-041")
@allure.title("Создание репозитория из шаблона")
@allure.severity(allure.severity_level.MINOR)
@pytest.mark.p3
def test_create_repo_by_template(authenticated_user_page: Page, test_user, created_template_repo):
    create_repo_page = CreateRepositoryPage(authenticated_user_page)
    repo_page = RepoPage(authenticated_user_page)
    repo_name = unique_name(prefix="repo")
    template_repo_name = created_template_repo["repo_name"]
    username = test_user["login"]

    with allure.step("Создать репозиторий из шаблона"):
        create_repo_page.open()

        create_repo_page.fill_repo_name_field(repo_name)
        create_repo_page.repo_template.open()
        create_repo_page.repo_template.select(created_template_repo["repo_id"])
        create_repo_page.select_checkbox_git_content()
        create_repo_page.click_repo_create_button()

    with allure.step("Проверить содержимое созданного репозитория"):
        repo_page.check_url(f"/{username}/{repo_name}")
        repo_page.repo_header.repo_name_in_header_is_displayed(repo_name=repo_name, username=username)
        repo_page.specified_file_in_list(".gitignore")
        repo_page.specified_file_in_list("LICENSE")
        repo_page.specified_file_in_list("README.md")
        repo_page.check_readme_title(template_repo_name)
        repo_page.check_readme_text(created_template_repo["description"])
        repo_page.repo_header.check_created_by_repo_text(owner_template=username, repo_template=template_repo_name)


@allure.testcase("TC-R-042")
@allure.title("Создание репозитория с набором меток (Issue Labels)")
@allure.severity(allure.severity_level.MINOR)
@pytest.mark.p3
@pytest.mark.parametrize(
    "labels_template, label_item",
    [
        pytest.param("Advanced", "Kind/Bug", id="advanced_labels"),
        pytest.param("Default", "help wanted", id="default_labels"),
    ],
)
def test_create_repo_with_label_template(authenticated_user_page: Page, test_user, labels_template, label_item):
    create_repo_page = CreateRepositoryPage(authenticated_user_page)
    repo_issues_page = RepoIssuesPage(authenticated_user_page)

    username = test_user["login"]
    repo_name = unique_name(prefix="repo")

    with allure.step("Создать репозиторий с набором меток"):
        create_repo_page.open()
        create_repo_page.fill_repo_name_field(repo_name)
        create_repo_page.issue_labels.open()
        create_repo_page.issue_labels.select(labels_template)
        create_repo_page.click_repo_create_button()

    with allure.step("Проверить, что метки добавлены в репозиторий"):
        repo_issues_page.open(username=username, repo_name=repo_name)
        repo_issues_page.open_labels_dropdown()
        repo_issues_page.labels_item_should_be_visible(label_item)


@allure.testcase("TC-R-046")
@allure.title("Создание репозитория из шаблона с метками задач")
@allure.severity(allure.severity_level.MINOR)
@pytest.mark.p3
def test_create_repo_by_template_with_label(authenticated_user_page: Page, test_user, created_template_repo_with_label):
    create_repo_page = CreateRepositoryPage(authenticated_user_page)
    repo_issues_page = RepoIssuesPage(authenticated_user_page)
    repo_page = RepoPage(authenticated_user_page)

    username = test_user["login"]
    repo_name = unique_name(prefix="repo")

    with allure.step("Создать репозиторий из шаблона с копированием меток"):
        create_repo_page.open()
        create_repo_page.fill_repo_name_field(repo_name)
        create_repo_page.repo_template.open()
        create_repo_page.repo_template.select(created_template_repo_with_label["repo_id"])
        create_repo_page.select_checkbox_labels_issues()
        create_repo_page.click_repo_create_button()
        repo_page.check_url(f"/{username}/{repo_name}")

    with allure.step("Проверить, что метки шаблона добавлены"):
        repo_issues_page.open(username=username, repo_name=repo_name)
        repo_issues_page.open_labels_dropdown()
        repo_issues_page.labels_item_should_be_visible(created_template_repo_with_label["labels"][0])
        repo_issues_page.labels_item_should_be_visible(created_template_repo_with_label["labels"][1])


@allure.testcase("TC-R-012")
@allure.title("Приватный репозиторий недоступен другому юзеру")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.p1
def test_private_repo_is_inaccessible_to_another_user(
    authenticated_second_user_page: Page, created_private_repo, test_user
):
    repo_page = RepoPage(authenticated_second_user_page)
    not_found_page = NotFoundErrorPage(authenticated_second_user_page)
    with allure.step("Открыть приватный репозиторий под другим пользователем"):
        repo_page.open(username=test_user["login"], repo_name=created_private_repo["repo_name"])

    with allure.step("Проверить, что репозиторий недоступен"):
        not_found_page.check_title_text()
        not_found_page.check_description_text()


@allure.testcase("TC-R-013")
@allure.title("Создание репозитория с readme")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.p1
def test_create_repo_with_readme_file(authenticated_user_page: Page, test_user):
    create_repo_page = CreateRepositoryPage(authenticated_user_page)
    repo_page = RepoPage(authenticated_user_page)
    repo_name = unique_name(prefix="user")

    with allure.step("Создать репозиторий с README"):
        create_repo_page.open()
        create_repo_page.fill_repo_name_field(repo_name)

        create_repo_page.select_checkbox_initialization_repo()

        create_repo_page.click_repo_create_button()
    with allure.step("Проверить, что репозиторий создан с README"):
        repo_page.check_url(f"/{test_user['login']}/{repo_name}")
        repo_page.repo_header.repo_name_in_header_is_displayed(username=test_user["login"], repo_name=repo_name)

        repo_page.specified_file_in_list("README.md")
        repo_page.readme_content_is_displayed()


@allure.testcase("TC-R-014")
@allure.title("Создание репозитория с readme + gitignore")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.p1
def test_create_repo_with_gitignore_and_readme_file(authenticated_user_page: Page, test_user):
    create_repo_page = CreateRepositoryPage(authenticated_user_page)
    repo_page = RepoPage(authenticated_user_page)
    repo_name = unique_name(prefix="repo")

    with allure.step("Создать репозиторий с .gitignore и README"):
        create_repo_page.open()
        create_repo_page.fill_repo_name_field(repo_name)

        create_repo_page.gitignore_dropdown.open()
        gitignore_name = create_repo_page.gitignore_dropdown.select_random_item()
        print(f"Выбрано: gitignore={gitignore_name!r}")

        create_repo_page.select_checkbox_initialization_repo()

        create_repo_page.click_repo_create_button()
    with allure.step("Проверить, что репозиторий создан с .gitignore и README"):
        repo_page.check_url(f"/{test_user['login']}/{repo_name}")
        repo_page.repo_header.repo_name_in_header_is_displayed(username=test_user["login"], repo_name=repo_name)
        repo_page.specified_file_in_list(".gitignore")
        repo_page.specified_file_in_list("README.md")

        repo_page.readme_content_is_displayed()


@allure.testcase("TC-R-015")
@allure.title("Создание репозитория с readme + license")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.p1
def test_create_repo_with_license_and_readme_file(authenticated_user_page: Page, test_user):
    create_repo_page = CreateRepositoryPage(authenticated_user_page)
    repo_page = RepoPage(authenticated_user_page)
    repo_name = unique_name(prefix="repo")

    with allure.step("Создать репозиторий с лицензией и README"):
        create_repo_page.open()
        create_repo_page.fill_repo_name_field(repo_name)

        create_repo_page.license_dropdown.open()
        license_name = create_repo_page.license_dropdown.select_random_item()
        print(f"Выбрано: license={license_name!r}")

        create_repo_page.select_checkbox_initialization_repo()

        create_repo_page.click_repo_create_button()
    with allure.step("Проверить, что репозиторий создан с лицензией и README"):
        repo_page.check_url(f"/{test_user['login']}/{repo_name}")
        repo_page.repo_header.repo_name_in_header_is_displayed(username=test_user["login"], repo_name=repo_name)
        repo_page.specified_file_in_list("LICENSE")
        repo_page.specified_file_in_list("README.md")
        repo_page.readme_content_is_displayed()


@allure.testcase("TC-R-016")
@allure.title("Создание репозитория с readme + gitignore + license")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.p1
def test_create_repo_with_license_readme_and_gitignore_files(authenticated_user_page: Page, test_user):
    create_repo_page = CreateRepositoryPage(authenticated_user_page)
    repo_page = RepoPage(authenticated_user_page)
    repo_name = unique_name(prefix="repo")

    with allure.step("Создать репозиторий с лицензией, .gitignore и README"):
        create_repo_page.open()
        create_repo_page.fill_repo_name_field(repo_name)

        create_repo_page.gitignore_dropdown.open()
        gitignore_name = create_repo_page.gitignore_dropdown.select_random_item()
        create_repo_page.press_esc()

        create_repo_page.license_dropdown.open()
        license_name = create_repo_page.license_dropdown.select_random_item()
        print(f"Выбрано: gitignore={gitignore_name!r}, license={license_name!r}")

        create_repo_page.select_checkbox_initialization_repo()

        create_repo_page.click_repo_create_button()
    with allure.step("Проверить, что репозиторий создан с лицензией, .gitignore и README"):
        repo_page.check_url(f"/{test_user['login']}/{repo_name}")
        repo_page.repo_header.repo_name_in_header_is_displayed(username=test_user["login"], repo_name=repo_name)
        repo_page.specified_file_in_list("LICENSE")
        repo_page.specified_file_in_list(".gitignore")
        repo_page.specified_file_in_list("README.md")
        repo_page.readme_content_is_displayed()


@pytest.mark.parametrize(
    "input_branch, expected_branch, title",
    [
        pytest.param(
            "tests-master",
            "tests-master",
            "Создание репозитория с нестандартным default branch",
            id="custom_branch",
            marks=[pytest.mark.p1, allure.testcase("TC-R-017")],
        ),
        pytest.param(
            "",
            "main",
            "Пустой default branch",
            id="empty_field_in_default_branch_field",
            marks=[pytest.mark.p3, allure.testcase("TC-R-037")],
        ),
    ],
)
@allure.title("{title}")
def test_create_repo_default_branch(authenticated_user_page: Page, test_user, input_branch, expected_branch, title):
    create_repo_page = CreateRepositoryPage(authenticated_user_page)
    repo_page = RepoPage(authenticated_user_page)
    repo_name = unique_name(prefix="repo")

    with allure.step("Создать репозиторий с указанной веткой по умолчанию"):
        create_repo_page.open()
        create_repo_page.fill_repo_name_field(repo_name)

        create_repo_page.select_checkbox_initialization_repo()

        create_repo_page.fill_default_branch_field(input_branch)

        create_repo_page.click_repo_create_button()
    with allure.step("Проверить ветку по умолчанию и содержимое репозитория"):
        repo_page.check_url(f"/{test_user['login']}/{repo_name}")
        repo_page.repo_header.repo_name_in_header_is_displayed(username=test_user["login"], repo_name=repo_name)
        repo_page.branch_dropdown_button_is_displayed()
        repo_page.check_branch_dropdown_button_text(expected_branch)
        repo_page.specified_file_in_list("README.md")
        repo_page.readme_content_is_displayed()


@allure.testcase("TC-R-018")
@allure.title("Создание репозитория в организации")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.p1
def test_create_repo_in_organization(authenticated_user_page: Page, created_public_organization_by_user):
    create_repo_page = CreateRepositoryPage(authenticated_user_page)
    repo_page = RepoPage(authenticated_user_page)
    repo_name = unique_name(prefix="repo")
    org_name = created_public_organization_by_user["name"]

    with allure.step("Создать репозиторий в организации"):
        create_repo_page.open()

        create_repo_page.owner_field_click()
        create_repo_page.select_owner(org_name)

        create_repo_page.fill_repo_name_field(repo_name)
        create_repo_page.click_repo_create_button()

    with allure.step("Проверить, что репозиторий создан в организации"):
        repo_page.check_url(f"/{org_name}/{repo_name}")
        repo_page.repo_header.repo_name_in_header_is_displayed(username=org_name, repo_name=repo_name)


@allure.testcase("TC-R-024")
@allure.title("Организация без прав на создание репо")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.p2
def test_repo_create_without_creation_rights(
    authenticated_user_page: Page, created_organization_without_creation_rights, test_user
):
    create_repo_page = CreateRepositoryPage(authenticated_user_page)
    org_name = created_organization_without_creation_rights["name"]

    with allure.step("Открыть список владельцев в форме создания репозитория"):
        create_repo_page.open()

        create_repo_page.owner_field_click()
    with allure.step("Проверить доступных владельцев"):
        create_repo_page.owner_is_selectable(test_user["login"])
        create_repo_page.owner_is_not_selectable(org_name)


@allure.testcase("TC-R-010")
@allure.title("Создание публичного репозитория")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.p1
def test_public_repo_is_accessible_to_another_user(
    authenticated_second_user_page: Page, created_public_repo, test_user
):
    repo_page = RepoPage(authenticated_second_user_page)
    user_login = test_user["login"]
    repo_name = created_public_repo["repo_name"]
    with allure.step("Открыть публичный репозиторий под другим пользователем"):
        repo_page.open(username=user_login, repo_name=repo_name)

    with allure.step("Проверить, что репозиторий доступен"):
        repo_page.repo_header.repo_name_in_header_is_displayed(repo_name=repo_name, username=user_login)
        repo_page.check_url(f"/{test_user['login']}/{repo_name}")


@allure.testcase("TC-R-040")
@allure.title("Создание репозитория с описанием")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.p2
def test_create_repo_with_description(authenticated_user_page: Page, test_user):
    create_repo_page = CreateRepositoryPage(authenticated_user_page)
    repo_page = RepoPage(authenticated_user_page)
    repo_name = unique_name(prefix="repo")
    repo_description = unique_name(prefix="description")

    with allure.step("Создать репозиторий с описанием"):
        create_repo_page.open()

        create_repo_page.fill_repo_name_field(repo_name)
        create_repo_page.fill_repo_description(repo_description)
        create_repo_page.select_checkbox_initialization_repo()

        create_repo_page.click_repo_create_button()
    with allure.step("Проверить, что репозиторий создан с описанием"):
        repo_page.repo_header.repo_name_in_header_is_displayed(repo_name=repo_name, username=test_user["login"])
        repo_page.check_repo_description_text(repo_description)
        repo_page.check_url(f"/{test_user['login']}/{repo_name}")


@allure.testcase("TC-R-045")
@allure.title("Описание репозитория: ввод ограничен 2048 символами")
@allure.severity(allure.severity_level.MINOR)
@pytest.mark.p3
def test_trying_create_repo_with_exceeding_description_value(authenticated_user_page: Page, test_user):
    create_repo_page = CreateRepositoryPage(authenticated_user_page)
    repo_page = RepoPage(authenticated_user_page)
    repo_name = unique_name(prefix="repo")
    description = value_with_length(3000)

    with allure.step("Заполнить форму с описанием длиннее максимума"):
        create_repo_page.open()

        create_repo_page.fill_repo_name_field(repo_name)
        create_repo_page.fill_repo_description(description)
        create_repo_page.repo_description_value_should_be_equal(description[:2048])
        create_repo_page.select_checkbox_initialization_repo()
    with allure.step("Создать репозиторий"):
        create_repo_page.click_repo_create_button()

    with allure.step("Проверить, что описание обрезано до максимума"):
        repo_page.check_url(f"/{test_user['login']}/{repo_name}")
        repo_page.check_repo_description_text(description[:2048])


@allure.testcase("TC-R-044")
@allure.title("Default branch длиннее максимума (101 символ)")
@allure.severity(allure.severity_level.MINOR)
@pytest.mark.p3
def test_create_repo_with_value_exceeding_maximum_for_default_branch(authenticated_user_page: Page):
    create_repo_page = CreateRepositoryPage(authenticated_user_page)
    repo_name = unique_name(prefix="repo")
    default_branch = value_with_length(101)

    with allure.step("Попытаться создать репозиторий с веткой длиннее максимума"):
        create_repo_page.open()

        create_repo_page.fill_repo_name_field(repo_name)
        create_repo_page.fill_default_branch_field(default_branch)
        create_repo_page.select_checkbox_initialization_repo()
        create_repo_page.click_repo_create_button()

    with allure.step("Проверить, что репозиторий не создан и показана ошибка"):
        create_repo_page.check_url("/repo/create")
        create_repo_page.error_message_has_text("form.DefaultBranch должен содержать максимум 100 символов.")


@allure.testcase("TC-R-043")
@allure.title("Default branch максимальной длины (100 символов)")
@allure.severity(allure.severity_level.MINOR)
@pytest.mark.p3
def test_create_repo_with_default_branch_upper_limit_value(authenticated_user_page: Page, test_user):
    create_repo_page = CreateRepositoryPage(authenticated_user_page)
    repo_page = RepoPage(authenticated_user_page)
    repo_name = unique_name(prefix="repo")
    default_branch = value_with_length(100)

    with allure.step("Создать репозиторий с веткой максимальной длины"):
        create_repo_page.open()

        create_repo_page.fill_repo_name_field(repo_name)
        create_repo_page.fill_default_branch_field(default_branch)
        create_repo_page.select_checkbox_initialization_repo()
        create_repo_page.click_repo_create_button()

    with allure.step("Проверить, что репозиторий создан с этой веткой"):
        repo_page.check_url(f"/{test_user['login']}/{repo_name}")
        repo_page.check_branch_dropdown_button_text(default_branch)
