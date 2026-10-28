[![Gitea CI](https://github.com/GunKel1y/gitea-qa-automation/actions/workflows/actions.yaml/badge.svg)](https://github.com/GunKel1y/gitea-qa-automation/actions/workflows/actions.yaml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![Python](https://img.shields.io/badge/python-3.12-blue.svg)
![pytest](https://img.shields.io/badge/pytest-redbluegreen.svg)
[![Allure Report](https://img.shields.io/badge/Allure-report-8A2BE2)](https://gunkel1y.github.io/gitea-qa-automation/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

# gitea-qa-automation

Портфолио-проект по автоматизации тестирования [Gitea](https://about.gitea.com) 1.26.2.

## Принципы

- **Изоляция.** Каждый тест создаёт своего пользователя и свои данные через API Gitea и удаляет их после завершения. Тесты не зависят друг от друга и от порядка запуска.
- **Уникальные данные.** Имена и логины создаются через `unique_name`, поэтому параллельные тесты не пересекаются.
- **Предусловия через API.** Интерфейс используется только там, где он и есть предмет проверки: так тесты быстрее и падают только по своей причине.
- **Стенд как код.** Gitea и PostgreSQL описаны в `docker-compose.yaml`; стенд поднимается с нуля, администратор создаётся автоматически. Тесты запускаются в контейнере.
- **Параллельность.** Тесты запускаются через `pytest-xdist` (по умолчанию 4 воркера).
- **Читаемость.** Page Object Model с компонентами, web-first проверки через `expect`.
- **Связь с тест-дизайном.** Каждый автоматизированный кейс из `docs/test-design.md` привязан к тесту через `@allure.testcase`. Приоритет задаётся одним маркером `p0`-`p3` на тест.
- **Наблюдаемость.** Шаги тестов описаны в отчёте Allure (`allure.step`, методы страниц размечены декоратором `step`), у каждого теста есть читаемое название, `epic` по модулю и `severity`. Секретные значения в шагах заменяются на `***`.

## Технологии

- **Язык и тесты:** Python 3.12, Pytest
- **UI:** Playwright (sync)
- **API-предусловия:** `requests`
- **Параллельный запуск:** pytest-xdist
- **Качество кода:** Ruff
- **Отчёт:** allure-pytest, Allure Report 2
  - Публикуется на GitHub Pages: https://gunkel1y.github.io/gitea-qa-automation/
- **Стенд:** Docker, Docker Compose, Gitea, PostgreSQL 16
- **CI:** GitHub Actions

## Покрытие

В тест-дизайне 97 кейсов, автоматизировано 82 (85%). Это 85 тестов с учётом параметризации.

| Модуль | Автоматизировано | Всего |
|--------|------------------|-------|
| Auth | 27 | 27 |
| Repository | 30 | 30 |
| Issues | 25 | 25 |
| Pull Requests | 0 | 15 (в планах) |

Подробности, матрицы «поле × вид проверки» и трассировка кейс -> автотест: [docs/test-design.md](docs/test-design.md).

## Архитектура

### Page Object Model и компоненты

Страницы (`pages/`) наследуются от `BasePage`, в котором лежат общие проверки и шапка сайта. Повторяющиеся части интерфейса вынесены в компоненты (`components/`), страницы собираются из них (композиция).

```python
class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.global_header = GlobalHeader(page)
        ...
```

Страницы репозитория лежат отдельно, в `pages/repo/`. Компоненты: `GlobalHeader`, `RepoHeader`, `CommentForm`, `IssueMetadata`, `SearchDropdown`.

### Фикстуры

Фикстуры в `conftest.py` готовят предусловия через API и убирают данные после теста (`yield` и удаление). Часть данных не удаляется отдельно, а уходит вместе с владельцем: метки и этапы удаляются вместе с репозиторием, репозитории и организации вместе с пользователем или явным вызовом в фикстуре.

| Фикстура | Что делает |
|----------|------------|
| `admin_token` | токен администратора, создаётся один раз на воркер (`session`, `autouse`), в конце сессии удаляется |
| `test_user`, `second_test_user` | пользователь со случайными данными, удаляется после теста |
| `authenticated_user_page`, `authenticated_second_user_page` | страница с залогиненным пользователем (вход через API-запрос, без UI), контекст закрывается после теста |
| `delete_user_after_registration` | готовит данные для теста регистрации и удаляет пользователя после него |
| `created_public_repo`, `created_private_repo`, `created_template_repo`, `created_template_repo_with_label` | репозитории разных типов |
| `created_public_organization_by_user`, `created_organization_without_creation_rights` | организации |
| `created_repo_issue`, `created_repo_issue_with_label`, `created_closed_repo_issue`, `created_timeline_comment` | задачи и комментарии |
| `created_repo_label`, `created_milestone` | метка и этап в публичном репозитории |
| `adding_collaboration_for_repo_with_admin_permission`, `disabling_ability_add_issue_to_repo` | настройка прав и возможностей репозитория |

### API-клиент и тестовые данные

- `helpers/api_client.py`: функции для API Gitea (пользователи, репозитории, организации и команды, задачи, метки, этапы, комментарии).
- `helpers/test_data.py`: генерация данных: `unique_name`, `random_password`, `random_email`, значения заданной длины для граничных проверок.

## Быстрый старт

Нужны Git и Docker с Compose.

```
git clone https://github.com/GunKel1y/gitea-qa-automation.git
cd gitea-qa-automation
cp .env.example .env
docker compose run --rm --build tests
```

Значения из `.env.example` подходят для локального запуска. Файл `.env` не попадает в git.

## Конфигурация

### Переменные окружения (`.env`)

| Переменная | Назначение |
|------------|------------|
| `GITEA_ADMIN_LOGIN`, `GITEA_ADMIN_PASSWORD`, `GITEA_ADMIN_EMAIL` | администратор Gitea, создаётся при запуске стенда |
| `DATABASE_NAME`, `DATABASE_USER`, `DATABASE_PASSWORD` | база данных PostgreSQL |
| `USER_UID`, `USER_GID` | UID и GID пользователя в контейнере Gitea (по умолчанию 1000) |

Адреса Gitea для контейнера с тестами задаёт сам `docker-compose.yaml`.

### Pytest

Настройки в `pytest.ini`: каталог тестов `tests`, подробный вывод, `--strict-markers`. Маркеры приоритета: `p0` (критический), `p1` (высокий), `p2` (средний), `p3` (низкий).

### Ruff

Линтер и форматтер настроены в `ruff.toml`: длина строки 120, правила `F`, `E`, `W`, `I`, `UP`, `B` (`E501` отключено).

Локальная проверка:

```
ruff check .
ruff format --check .
```

## Запуск тестов

Все тесты (стенд поднимется сам, 4 воркера):

```
docker compose run --rm --build tests
```

Команда собирает образ с тестами (первая сборка занимает несколько минут: ставятся браузеры Playwright), поднимает PostgreSQL и Gitea, создаёт администратора и запускает тесты.

Другие варианты: после `tests` указывается команда pytest.

```
docker compose run --rm tests pytest -m p0
docker compose run --rm tests pytest tests/test_auth.py -n 2
docker compose run --rm tests pytest -k "private"
```

После изменений в коде тестов нужен `--build`, иначе возьмётся старый образ.

Результаты Allure после прогона лежат на хосте в `./allure-results` (папка подключена к контейнеру томом и очищается при каждом запуске). Локально собрать отчёт можно через Allure CLI (нужна установленная утилита `allure`):

```
allure serve allure-results
```

Gitea остаётся запущенной на http://localhost:3000 (вход с данными администратора из `.env`). 

Остановить стенд: `docker compose down`; остановить и стереть данные: `docker compose down -v`.

## CI (GitHub Actions)

Два workflow:

**`.github/workflows/actions.yaml` («Gitea CI»)**

- запускается на каждый push и pull request в `main`; результаты прогонов видны во вкладке Actions;
- вручную (для владельца репозитория или в своём форке): Actions -> «Gitea CI» -> Run workflow, с выбором числа воркеров (1, 2 или 4; по умолчанию 4);
- джоба `ruff` проверяет код (`ruff check` и `ruff format --check`), джоба `tests` стартует только после неё;
- `tests` поднимает тот же compose-стенд, что и локальный запуск; при падении выводит логи `gitea-init`, Gitea и PostgreSQL;
- после прогона сохраняет `allure-results` как артефакт, в том числе при падении тестов.

**`.github/workflows/allure.yaml` («Allure Gitea»)**

- запускается после завершения «Gitea CI»;
- скачивает `allure-results`, подкладывает историю прошлого отчёта (чтобы работали тренды), собирает отчёт и сохраняет его артефактом `allure-report`;
- с ветки `main` публикует отчёт на GitHub Pages: https://gunkel1y.github.io/gitea-qa-automation/

Чтобы запустить CI в своём форке: включить Actions во вкладке Actions форка и в Settings -> Secrets and variables -> Actions добавить шесть секретов: `GITEA_ADMIN_LOGIN`, `GITEA_ADMIN_PASSWORD`, `GITEA_ADMIN_EMAIL`, `DATABASE_NAME`, `DATABASE_USER`, `DATABASE_PASSWORD` (значения как в `.env.example`). Секреты не копируются вместе с репозиторием. Публикация на Pages в форке потребует включить Pages (Settings -> Pages -> Source: GitHub Actions).

## Структура проекта

```
.
├── tests/                      # тесты по модулям системы
│   ├── test_auth.py            # авторизация и аутентификация
│   ├── test_registration.py    # регистрация
│   ├── test_repo.py            # репозитории
│   └── test_issues.py          # задачи
├── pages/                      # Page Object Model
│   ├── base_page.py
│   └── repo/                   # страницы репозитория
├── components/                 # переиспользуемые блоки страниц
├── helpers/
│   ├── api_client.py           # клиент API Gitea
│   ├── allure_helpers.py       # декоратор step для шагов Allure
│   └── test_data.py            # генерация тестовых данных
├── docs/test-design.md         # тест-дизайн
├── conftest.py                 # фикстуры
├── pytest.ini
├── ruff.toml                   # настройки линтера и форматтера
├── requirements.txt            # зависимости с зафиксированными версиями
├── Dockerfile                  # образ с тестами
├── docker-compose.yaml         # стенд: Gitea, PostgreSQL, тесты
├── .env.example                # образец настроек
├── LICENSE
└── .github/workflows/
    ├── actions.yaml            # Gitea CI: ruff и тесты
    └── allure.yaml             # Allure Gitea: отчёт и публикация на Pages
```

## Пример теста

```python
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
```

Фикстура-предусловие:

```python
@pytest.fixture()
def created_public_repo(test_user):
    """Создает публичный репозиторий, после теста удаляет"""
    repo_name = unique_name(prefix="repo")
    created_repo = create_repo(owner=test_user["login"], repo_name=repo_name, private=False)
    assert created_repo.ok, f"Ошибка создания публичного репозитория: {created_repo.status_code} {created_repo.text}"

    yield {"repo_name": repo_name}

    delete_repo(owner=test_user["login"], repo_name=repo_name)
```

## FAQ

**Изменил тесты, а в контейнере старое поведение:**
- Добавьте `--build`: без него используется ранее собранный образ.


**Не стартует стенд: порт 3000 занят:**
- Gitea публикуется на порт 3000 хоста. Остановите программу, которая его занимает, или поменяйте проброс `ports` у сервиса `gitea` в `docker-compose.yaml`.

**Нужен чистый стенд:**
- `docker compose down -v` удаляет контейнеры и тома (данные Gitea и PostgreSQL); при следующем запуске администратор создастся заново.
