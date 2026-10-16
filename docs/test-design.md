# Тест-дизайн: Gitea

Документ описывает тестовые сценарии для веб-интерфейса Gitea: что и как проверяется, с какими приоритетами и какие из сценариев автоматизированы.

## Содержание

- [Область тестирования и подход](#область-тестирования-и-подход)
- [Обозначения](#обозначения)
- [Сводка покрытия](#сводка-покрытия)
- [Матрицы «поле × вид проверки»](#матрицы-поле--вид-проверки)
- [Auth](#auth) · [Repository](#repository) · [Issues](#issues) · [Pull Requests](#pull-requests)
- [Трассируемость: кейс → автотест](#трассируемость-кейс--автотест)

## Область тестирования и подход

- **В охвате:** функциональное поведение UI и базовая безопасность (авторизация, права пользователей). Безопасность самой Gitea (XSS, экранирование HTML и т.п.) не проверяется.
- **Подход:** кейсы строятся по матрицам «поле × вид проверки» (пустое значение, границы, формат, дубль, несовпадение). Границы проверяются парой: валидная и невалидная сторона.
- **Автоматизация:** Python, Pytest, Playwright. Каждый автоматизированный кейс привязан к тесту (раздел «Трассируемость»).

## Обозначения

| Обозначение | Значение |
|-------------|----------|
| P0 - P3 | Приоритет: P0 наивысший (базовые сценарии модуля), P3 наименьший |
| Тип | `smoke`, `positive`, `negative`, `boundary`, `edge`, `security`, `permissions` |
| Авто | `да` - кейс автоматизирован, `нет` - не автоматизирован |
| ID | Идентификаторы стабильны и не переиспользуются, поэтому нумерация не сплошная |

## Сводка покрытия

Формула: `Scenario coverage % = автоматизированные кейсы / все кейсы × 100`. Всего кейсов: 96.

| Модуль | Автоматизировано | Всего | Покрытие |
|--------|------------------|-------|----------|
| Auth | 27               | 27 | 100%     |
| Repository | 27               | 29 | 93%      |
| Issues | 25               | 25 | 100%     |
| Pull Requests | 0                | 15 | 0%       |
| **Итого** | **79**           | **96** | **82%**  |

| Приоритет | Автоматизировано | Всего | Покрытие |
|-----------|------------------|-------|----------|
| P0 | 5                | 7 | 71%      |
| P1 | 24               | 32 | 75%      |
| P2 | 29               | 33 | 88%      |
| P3 | 21               | 24 | 88%      |

## Матрицы «поле × вид проверки»

Для каждой формы показано, каким кейсом закрыта каждая проверка поля. «—» означает, что проверка для поля не предусмотрена.

**Регистрация**

| Поле | Пусто | Мин. граница | Макс. граница | Формат / символы | Дубль | Несовпадение |
|------|-------|--------------|---------------|------------------|-------|--------------|
| username | A-032 | A-034a (ограничения нет) | A-034b, A-034c | A-033 | A-022 | — |
| email | A-036 | A-041 (ограничения нет) | A-039, A-040 | A-023, A-037, A-038 | A-031 | — |
| password | A-035 | 7: A-025; 8: A-027 | 256: A-026; 255: A-028 | — | — | A-024 |

**Создание репозитория**

| Поле | Пусто | Мин. граница | Макс. граница | Формат / символы | Дубль | Прочее |
|------|-------|--------------|---------------|------------------|-------|--------|
| Имя | R-020 | R-030 | R-031, R-032 | R-022, R-023a, R-023b, R-033, R-034 | R-021 | R-035 |
| Owner | — | — | — | — | — | R-001 (пользователь), R-018 (организация), R-024 (нет прав) |
| Видимость | — | — | — | — | — | R-010, R-011, R-012 |
| Инициализация | R-035 | — | — | — | — | R-013, R-014, R-015, R-016 |
| Default branch | R-037 | — (минимума нет) | R-043, R-044 | — | — | R-017 |
| Описание | R-001 (без описания) | — (пустое допустимо) | R-045 | — | — | R-040 |
| Шаблон, набор меток | — | — | — | — | — | R-041, R-042 |

**Создание issue**

| Поле | Пусто | Мин. граница | Макс. граница | Формат / символы | Прочее |
|------|-------|--------------|---------------|------------------|--------|
| Title | I-030 | I-001 (ограничения нет) | I-033 | — | — |
| Описание | I-001 (пустое принимается) | — (минимума нет) | — | — | I-010 (создание), I-012b (редактирование) |
| Метка, исполнитель, milestone при создании | — | — | — | — | I-036, I-037, I-038 |
| Права | — | — | — | — | I-040, I-041, I-042, I-043 |

## Auth

Логин, логаут, регистрация, доступ к защищённым страницам. Кейсов: 27, автоматизировано: 16.

| ID | P | Тип | Название | Предусловия | Шаги | Ожидаемый результат | Авто |
|----|---|-----|----------|-------------|------|---------------------|-----|
| TC-A-001 | P0 | smoke | **Успешный логин с валидными данными** | Юзер зарегистрирован | 1. Открыть /user/login<br>2. Ввести валидные username и password<br>3. Sign In | Редирект на дашборд, юзер авторизован, элементы шапки (профиль, аватар) отображают авторизованное состояние | да  |
| TC-A-002 | P0 | smoke | **Логаут** | Юзер авторизован | 1. Открыть меню профиля<br>2. Нажать Logout | Сессия завершена, редирект на главную/логин, попытка открыть защищённую страницу ведёт на логин | да  |
| TC-A-010 | P1 | positive | **Успешная регистрация нового юзера** | Username и email свободны | 1. Открыть /user/sign_up<br>2. Заполнить username/email/password/confirm валидными данными<br>3. Register | Юзер создан, авто-логин, редирект на `/`, баннер «Учётная запись успешно создана. Добро пожаловать!» | да  |
| TC-A-011 | P1 | positive | **Доступ к защищённой странице без авторизации отклонён** | Юзер не авторизован | 1. Перейти напрямую на защищённую страницу (в тесте `/repo/create`) | Редирект на `/user/login?redirect_to=%2Frepo%2Fcreate` | да  |
| TC-A-020 | P2 | negative | **Логин с неверным паролем** | Юзер зарегистрирован | 1. Открыть /user/login<br>2. Ввести valid username + неверный password<br>3. Sign In | Ошибка «Неверное имя пользователя или пароль.», форма логина остаётся, URL `/user/login`, юзер не авторизован | да  |
| TC-A-021 | P2 | security | **Логин с несуществующим username** | — | 1. Ввести несуществующий username + любой password<br>2. Sign In | Та же ошибка «Неверное имя пользователя или пароль.», что и в A-020: сообщение не раскрывает, существует ли юзер | да  |
| TC-A-022 | P2 | negative | **Регистрация с уже занятым username** | Username `existing_user` уже занят | 1. Заполнить форму регистрации с этим username<br>2. Register | Ошибка «Имя пользователя уже занято.», URL `/user/sign_up`, юзер не создан | да  |
| TC-A-023 | P2 | negative | **Регистрация с email без `@`** | — | 1. Заполнить форму, email=`notanemail`<br>2. Register | Форма не отправляется, URL остаётся `/user/sign_up`. Браузер показывает нативную подсказку HTML5-валидации (её нет в DOM, текст зависит от браузера и локали) | да  |
| TC-A-024 | P2 | negative | **Регистрация с несовпадающими password/confirm** | — | 1. Заполнить форму, password ≠ confirm password<br>2. Register | Ошибка «Пароли не совпадают.», URL `/user/sign_up` | да  |
| TC-A-025 | P2 | negative | **Регистрация с паролем короче минимальной длины (7 символов при минимуме 8)** | — | 1. Заполнить форму, password из 7 символов, confirm совпадает<br>2. Register | Ошибка «Пароль не может быть короче 8 символов.», URL `/user/sign_up` | да  |
| TC-A-026 | P2 | boundary | **Регистрация с паролем длиннее максимума (256 символов)** | — | 1. Заполнить форму, password из 256 символов, confirm совпадает<br>2. Register | Ошибка «Пароль должен содержать максимум 255 символов.», URL `/user/sign_up` | да  |
| TC-A-032 | P2 | negative | **Регистрация с пустым username** | — | 1. Заполнить форму, username пустой<br>2. Register | Форма не отправляется, URL `/user/sign_up`. Браузер показывает нативную подсказку о незаполненном поле (её нет в DOM; в тесте проверяется состояние поля `:invalid`, текст подсказки не проверяется) | да |
| TC-A-033 | P2 | negative | **Регистрация с недопустимыми символами в username (пробел, эмодзи, `/`)** | — | 1. Заполнить форму, username с недопустимым символом<br>2. Register | Баннер ошибки формы с текстом «Пользователь can only contain alphanumeric characters…» (текст частично на английском: перевод Gitea неполный), URL `/user/sign_up` | да |
| TC-A-035 | P2 | negative | **Регистрация с пустым паролем** | — | 1. Заполнить форму, password и confirm пустые<br>2. Register | Форма не отправляется, URL `/user/sign_up`. Браузер показывает нативную подсказку о незаполненном поле (её нет в DOM; в тесте проверяется состояние поля `:invalid`, текст подсказки не проверяется) | да |
| TC-A-036 | P2 | negative | **Регистрация с пустым email** | — | 1. Заполнить форму, email пустой<br>2. Register | Регистрация не проходит, URL `/user/sign_up` | да  |
| TC-A-037 | P2 | negative | **Регистрация с email без домена (`name@`)** | — | 1. Заполнить форму, email=`<имя>@`<br>2. Register | Регистрация не проходит, URL `/user/sign_up` | да  |
| TC-A-038 | P2 | negative | **Регистрация с email без локальной части (`@name.com`)** | — | 1. Заполнить форму, email=`@<имя>.com`<br>2. Register | Регистрация не проходит, URL `/user/sign_up` | да  |
| TC-A-027 | P3 | boundary | **Регистрация с паролем минимальной валидной длины (8 символов)** | — | 1. Заполнить форму, password из 8 символов<br>2. Register | Регистрация успешна (парная граница к A-025) | да  |
| TC-A-028 | P3 | boundary | **Регистрация с паролем максимальной валидной длины (255 символов)** | — | 1. Заполнить форму, password из 255 символов<br>2. Register | Регистрация успешна (парная граница к A-026) | да  |
| TC-A-030 | P3 | negative | **Логин с пустыми полями** | — | 1. Оставить username и password пустыми<br>2. Sign In | Форма логина остаётся, URL `/user/login` (форма не сабмитится) | да  |
| TC-A-031 | P3 | negative | **Регистрация с уже используемым email другим юзером** | Email уже используется другим юзером | 1. Заполнить форму с тем же email<br>2. Register | На этом инстансе дубль email отклоняется: «Этот адрес электронной почты уже используется.», URL `/user/sign_up` | да  |
| TC-A-034a | P3 | boundary | **Username из 1 символа (минимального ограничения длины нет)** | — | 1. Заполнить форму, username из 1 символа<br>2. Register | Регистрация успешна | да |
| TC-A-034b | P3 | boundary | **Username максимальной длины (40 символов)** | — | 1. Заполнить форму, username из 40 символов<br>2. Register | Регистрация успешна | да |
| TC-A-034c | P3 | boundary | **Username длиннее максимума (41 символ)** | — | 1. Заполнить форму, username из 41 символа<br>2. Register | Баннер ошибки формы «Пользователь должен содержать максимум 40 символов.», URL `/user/sign_up`, юзер не создан (профиль `/{login}` отдаёт 404) | да |
| TC-A-039 | P3 | boundary | **Регистрация с email максимальной валидной длины (254 символа)** | — | 1. Заполнить форму, email из 254 символов (валидный формат)<br>2. Register | Регистрация успешна (парная граница к A-040) | да  |
| TC-A-040 | P3 | boundary | **Регистрация с email длиннее максимума (255 символов)** | — | 1. Заполнить форму, email из 255 символов<br>2. Register | Ошибка «Адрес эл. почты должен содержать максимум 254 символов.», URL `/user/sign_up`, юзер не создан | да |
| TC-A-041 | P3 | boundary | **Регистрация с минимально короткой записью email (`1@ru`)** | — | 1. Заполнить форму, email=`1@ru`<br>2. Register | Регистрация проходит: минимальной длины email нет | да  |

## Repository

Создание репозитория: имя, владелец, видимость, инициализация (README, .gitignore, лицензия), default branch, описание, шаблон, набор меток. Кейсов: 29, автоматизировано: 22.

| ID | P | Тип | Название | Предусловия | Шаги | Ожидаемый результат | Авто |
|----|---|-----|----------|-------------|------|---------------------|------|
| TC-R-001 | P0 | smoke | **Создание репозитория с минимальным набором данных** | Юзер авторизован | 1. New Repository<br>2. Ввести валидное имя<br>3. Create | Репозиторий создан, редирект на `/<owner>/<repo>`, имя репозитория в шапке | да |
| TC-R-010 | P1 | positive | **Создание публичного репозитория** | Юзер авторизован; есть второй залогиненный пользователь | 1. New Repository<br>2. Оставить Private выключенным<br>3. Create<br>4. Открыть репозиторий вторым залогиненным пользователем | Репозиторий создан как публичный и доступен второму залогиненному пользователю | да |
| TC-R-011 | P1 | positive | **Создание приватного репозитория** | Юзер авторизован | 1. New Repository<br>2. Включить Private<br>3. Create | Репозиторий создан, статус приватности отображается в шапке | да |
| TC-R-012 | P1 | security | **Приватный репозиторий недоступен другому юзеру** | Репозиторий создан как private (TC-R-011) | 1. Залогиниться другим юзером<br>2. Перейти по прямой ссылке на репо | «404 Not Found», текст «Либо страница, которую вы пытаетесь открыть, не существует, либо у вас недостаточно прав для ее просмотра.» | да |
| TC-R-013 | P1 | positive | **Создание репозитория с readme** | Юзер авторизован | 1. New Repository<br>2. Включить "Initialize repository"<br>3. Create | Репозиторий создан, в списке файлов `README.md`, содержимое README отображается | да |
| TC-R-014 | P1 | positive | **Создание репозитория с readme + gitignore** | Юзер авторизован | 1. Включить readme<br>2. Выбрать шаблон .gitignore из выпадающего списка<br>3. Create | В списке файлов `.gitignore` и `README.md` | да |
| TC-R-015 | P1 | positive | **Создание репозитория с readme + license** | Юзер авторизован | 1. Включить readme<br>2. Выбрать лицензию из выпадающего списка<br>3. Create | В списке файлов `LICENSE` и `README.md` | да |
| TC-R-016 | P1 | positive | **Создание репозитория с readme + gitignore + license** | Юзер авторизован | 1. Включить readme<br>2. Выбрать .gitignore и лицензию из выпадающих списков<br>3. Create | В списке файлов `LICENSE`, `.gitignore` и `README.md` | да |
| TC-R-017 | P1 | positive | **Создание репозитория с нестандартным default branch** | Юзер авторизован | 1. Включить readme<br>2. Указать нестандартное имя branch (например, `develop`)<br>3. Create | Default branch = указанное имя, кнопка ветки показывает это имя, README на месте | да |
| TC-R-018 | P1 | positive | **Создание репозитория в организации** | Юзер — участник организации с правом создавать репо | 1. New Repository<br>2. Выбрать owner = организация<br>3. Create | Репозиторий создан под организацией, URL `/<org>/<repo>`, owner в шапке = организация | да |
| TC-R-020 | P2 | negative | **Создание репозитория с пустым именем** | Юзер авторизован | 1. New Repository<br>2. Оставить имя пустым<br>3. Create | Репозиторий не создан, URL `/repo/create`, форма остаётся | да |
| TC-R-021 | P2 | negative | **Создание репозитория с именем, которое уже существует у owner** | У юзера уже есть репозиторий с этим именем | 1. New Repository<br>2. Ввести то же имя<br>3. Create | Ошибка «Название репозитория уже используется.», репозиторий не создан | да |
| TC-R-022 | P2 | negative | **Создание репозитория с двумя точками в имени** | Юзер авторизован | 1. Ввести имя `..`<br>2. Create | Репозиторий не создан, URL `/repo/create`, форма остаётся (текст ошибки тестом не проверяется) | да |
| TC-R-023a | P2 | edge | **Эмодзи внутри имени заменяется дефисом** | Юзер авторизован | 1. New Repository<br>2. Ввести `test-⭐`<br>3. Create | Репозиторий создан с именем `test--` | да |
| TC-R-023b | P2 | negative | **Имя только из эмодзи отклоняется** | Юзер авторизован | 1. New Repository<br>2. Ввести `⭐`<br>3. Create | Репозиторий не создан, URL `/repo/create`, форма остаётся | да |
| TC-R-024 | P2 | permissions | **Организация без прав на создание репо** | Юзер — участник организации БЕЗ права создавать репо | 1. Попытаться создать репо от имени организации | В списке owner своя учётная запись выбираема, организация без права создавать репозитории недоступна для выбора | да |
| TC-R-040 | P2 | positive | **Создание репозитория с описанием** | Юзер авторизован | 1. New Repository<br>2. Ввести имя и описание<br>3. Включить инициализацию (README)<br>4. Create | Описание отображается на странице репозитория | да |
| TC-R-030 | P3 | boundary | **Имя минимальной длины (1 символ)** | Юзер авторизован | 1. Ввести имя из 1 символа<br>2. Create | Репозиторий с именем из 1 символа создан (пустой, показан гайд создания) | да |
| TC-R-031 | P3 | boundary | **Имя на границе максимальной длины (100 символов)** | Юзер авторизован | 1. Ввести имя из 100 символов<br>2. Create | Репозиторий с именем из 100 символов создан | да |
| TC-R-032 | P3 | boundary | **Имя длиннее максимума (101 символ) обрезается до 100** | Юзер авторизован | 1. Ввести имя из 101 символа<br>2. Create | Репозиторий создан с именем из 100 символов (лишний символ отброшен) | да |
| TC-R-033 | P3 | edge | **Имя с пробелом: пробел заменяется на дефис** | Юзер авторизован | 1. Ввести имя с пробелом<br>2. Create | Репозиторий создан, `a b` превращается в `a-b` | да |
| TC-R-034 | P3 | edge | **Имя со слэшем: слэш заменяется на дефис** | Юзер авторизован | 1. Ввести имя со слэшем<br>2. Create | Репозиторий создан, `a/b` превращается в `a-b` | да |
| TC-R-035 | P3 | edge | **Репозиторий без readme/gitignore/license — пустой** | Юзер авторизован | 1. New Repository, не включать readme<br>2. Create | Репозиторий создан пустым, показан гайд создания | да |
| TC-R-037 | P3 | edge | **Пустой default branch** | Юзер авторизован | 1. Включить readme<br>2. Очистить поле branch<br>3. Create | Пустое поле default branch: fallback на `main` | да |
| TC-R-041 | P3 | positive | **Создание репозитория из шаблона** | Существует репозиторий-шаблон | 1. New Repository<br>2. Выбрать шаблон<br>3. Create | Файлы шаблона присутствуют в новом репозитории | нет |
| TC-R-042 | P3 | positive | **Создание репозитория с набором меток (Issue Labels)** | Юзер авторизован | 1. New Repository<br>2. Выбрать набор меток из выпадающего списка<br>3. Create | Метки набора доступны в Issues нового репозитория. Проверяются встроенные наборы из выпадающего списка | нет |
| TC-R-043 | P3 | boundary | **Default branch максимальной длины (100 символов)** | Юзер авторизован | 1. Включить readme<br>2. Указать branch из 100 символов<br>3. Create | Репозиторий создан, default branch = указанное имя из 100 символов (парная граница к R-044) | да |
| TC-R-044 | P3 | boundary | **Default branch длиннее максимума (101 символ)** | Юзер авторизован | 1. Включить readme<br>2. Указать branch из 101 символа<br>3. Create | Репозиторий не создан, показана ошибка о превышении максимальной длины (100 символов) default branch | да |
| TC-R-045 | P3 | boundary | **Описание репозитория: ввод ограничен 2048 символами** | Юзер авторизован | 1. New Repository<br>2. Ввести описание длиннее 2048 символов | Поле принимает не более 2048 символов, остальной ввод блокируется. Пустое описание допустимо (R-001) | да |

## Issues

Создание, закрытие и переоткрытие issue, редактирование, метки, исполнитель, milestone, комментарии, права других пользователей. Кейсов: 25, автоматизировано: 15.

| ID | P | Тип | Название | Предусловия | Шаги | Ожидаемый результат | Авто |
|----|---|-----|----------|-------------|------|---------------------|------|
| TC-I-001 | P0 | smoke | **Создание issue с минимальными данными** | Репозиторий существует, issues включены | 1. New Issue<br>2. Ввести title<br>3. Submit | Issue создана, статус «Открыто», в заголовке отображается номер | да |
| TC-I-002 | P0 | smoke | **Закрытие issue** | Issue открыта | 1. Открыть issue<br>2. Close Issue | Статус «Закрыто», кнопка меняется на «Открыть снова» | да |
| TC-I-010 | P1 | positive | **Создание issue с title и описанием** | Репозиторий существует | 1. New Issue<br>2. Заполнить title и description<br>3. Submit | Issue создана, заголовок и первый комментарий (описание) отображаются | да |
| TC-I-011 | P1 | positive | **Переоткрытие закрытой issue** | Issue закрыта | 1. Открыть issue<br>2. Reopen | Статус «Открыто», кнопка меняется на «Закрыть задачу» | да |
| TC-I-012a | P1 | positive | **Редактирование title issue** | Issue существует, автор: текущий юзер | 1. Открыть issue<br>2. Edit<br>3. Изменить title<br>4. Save | Новый title сохранён и отображается | да |
| TC-I-012b | P1 | positive | **Редактирование описания issue** | Issue существует, автор: текущий юзер | 1. Открыть issue<br>2. Edit у описания<br>3. Изменить текст<br>4. Save | Новый текст описания сохранён и отображается | да |
| TC-I-013 | P1 | positive | **Добавление метки** | Issue существует, в репо есть labels | 1. Открыть issue<br>2. Добавить label через sidebar | Label отображается на issue | да |
| TC-I-014 | P1 | positive | **Снятие метки** | На issue есть label | 1. Открыть issue<br>2. Убрать label через sidebar | Label больше не отображается | да |
| TC-I-015 | P1 | positive | **Назначение исполнителя** | Issue существует, есть collaborator | 1. Открыть issue<br>2. Назначить assignee | Assignee отображается на issue | да |
| TC-I-016 | P1 | positive | **Привязка к milestone** | Issue существует, milestone создан | 1. Открыть issue<br>2. Привязать milestone | Milestone отображается на issue | да |
| TC-I-017 | P1 | positive | **Добавление комментария** | Issue существует | 1. Открыть issue<br>2. Написать комментарий<br>3. Comment | Комментарий в треде с автором и временем | да |
| TC-I-018 | P1 | positive | **Редактирование своего комментария** | Комментарий существует, автор — текущий юзер | 1. Открыть меню комментария<br>2. Edit<br>3. Изменить текст<br>4. Save | Изменения сохранены, отображается отметка "edited" | да |
| TC-I-019 | P1 | positive | **Удаление своего комментария (с подтверждением)** | Комментарий существует, автор: текущий юзер | 1. Открыть меню комментария<br>2. Delete<br>3. Подтвердить в диалоге | Комментарий удалён из треда | да |
| TC-I-019b | P1 | positive | **Отмена удаления своего комментария** | Комментарий существует, автор: текущий юзер | 1. Открыть меню комментария<br>2. Delete<br>3. Отменить в диалоге | Диалог подтверждения закрыт, комментарий остаётся в треде | да |
| TC-I-020 | P1 | positive | **Комментарий в закрытой issue** | Issue закрыта | 1. Открыть закрытую issue<br>2. Написать комментарий<br>3. Comment | Комментарий добавляется, статус issue остаётся Closed | да |
| TC-I-030 | P2 | negative | **Создание issue с пустым title** | Репозиторий существует | 1. New Issue<br>2. Оставить title пустым<br>3. Submit | Форма не отправляется, issue не создана: URL остаётся `/{owner}/{repo}/issues/new`, поле title в состоянии `:invalid`. Браузер показывает нативную подсказку HTML5 (её нет в DOM, текст в тесте не проверяется) | да |
| TC-I-032 | P2 | negative | **Создание issue в репозитории с отключёнными issues** | В репозитории отключены Issues (Settings → Issues off) | 1. Попытаться перейти на /repo/issues/new | Страница 404 (заголовок и описание ошибки проверяются): issues недоступны | да |
| TC-I-036 | P2 | positive | **Создание issue с меткой** | В репозитории есть метки | 1. New Issue<br>2. Title<br>3. Выбрать метку в sidebar<br>4. Submit | Issue создана с меткой | да |
| TC-I-037 | P2 | positive | **Создание issue с исполнителем** | Есть collaborator | 1. New Issue<br>2. Title<br>3. Выбрать исполнителя<br>4. Submit | Issue создана с исполнителем | да |
| TC-I-038 | P2 | positive | **Создание issue с milestone** | Milestone создан | 1. New Issue<br>2. Title<br>3. Выбрать milestone<br>4. Submit | Issue создана с milestone | да |
| TC-I-040 | P2 | permissions | **Чужой юзер не может редактировать title и описание чужой issue** | Issue создана юзером A; юзер B не коллаборатор | 1. Залогиниться юзером B<br>2. Открыть issue | Кнопка Edit недоступна | да |
| TC-I-041 | P2 | permissions | **Чужой юзер не может закрыть чужую issue** | Issue создана юзером A; юзер B не коллаборатор | 1. Залогиниться юзером B<br>2. Открыть issue | Кнопка закрытия недоступна | да |
| TC-I-042 | P2 | permissions | **Чужой юзер не может редактировать и удалять чужой комментарий** | Комментарий оставлен юзером A; юзер B не коллаборатор | 1. Залогиниться юзером B<br>2. Открыть меню комментария | Пункты Edit и Delete недоступны | да |
| TC-I-043 | P2 | permissions | **Чужой юзер может оставить комментарий в публичном репозитории** | Публичный репозиторий; юзер B не коллаборатор | 1. Залогиниться юзером B<br>2. Открыть issue<br>3. Написать комментарий | Комментарий добавлен (ограничения на комментирование нет) | да |
| TC-I-033 | P3 | boundary | **Title issue: ввод ограничен максимальной длиной** | Репозиторий существует | 1. New Issue<br>2. Ввести title длиннее лимита<br>3. Submit | Поле не позволяет ввести больше 255 символов; issue с title длиной 255 создаётся. Минимального ограничения нет | да |

## Pull Requests

Создание PR, способы merge, ревью, конфликты, закрытие и переоткрытие, права пользователей. Кейсов: 15, автоматизировано: 0.

| ID | P | Тип | Название | Предусловия | Шаги | Ожидаемый результат | Авто |
|----|---|-----|----------|-------------|------|---------------------|------|
| TC-P-001 | P0 | smoke | **Создание PR из ветки с изменениями** | В репо есть ветка `feature-1` с коммитом, отличным от `main` | 1. New Pull Request, base=main, compare=feature-1<br>2. Create | PR создан, статус Open, показан diff | нет |
| TC-P-002 | P0 | smoke | **Обычный merge PR без конфликтов** | PR открыт, без конфликтов | 1. Открыть PR<br>2. Merge Pull Request | PR получает статус Merged, коммит появляется в base-ветке | нет |
| TC-P-010 | P1 | positive | **Squash merge** | PR открыт, без конфликтов, squash разрешён в настройках | 1. Merge → Squash and merge | PR смерджен одним коммитом в base-ветке | нет |
| TC-P-011 | P1 | positive | **Rebase merge** | PR открыт, без конфликтов, rebase разрешён в настройках | 1. Merge → Rebase and merge | PR смерджен через rebase, коммиты добавлены в base-ветку без merge-коммита | нет |
| TC-P-012 | P1 | positive | **Ревью PR: approve** | PR открыт, у второго юзера есть права на review | 1. Второй юзер → Review → Approve | PR помечен как approved этим ревьюером | нет |
| TC-P-013 | P1 | positive | **Ревью PR: request changes** | PR открыт | 1. Review → Request Changes → оставить комментарий | PR помечен "changes requested"; если включена branch protection — merge блокируется до устранения | нет |
| TC-P-014 | P1 | positive | **Комментарий к конкретной строке диффа** | PR открыт | 1. Открыть вкладку Files changed<br>2. Навести на строку → добавить комментарий | Комментарий отображается привязанным к конкретной строке | нет |
| TC-P-015 | P1 | positive | **Разрешение конфликта и повторный merge** | PR с конфликтом (TC-P-021), конфликт разрешён коммитом в compare-ветку | 1. Обновить PR<br>2. Merge | Merge проходит успешно | нет |
| TC-P-016 | P1 | positive | **Закрытие PR без мерджа** | PR открыт | 1. Close Pull Request | Статус Closed (без merge), ветка не тронута | нет |
| TC-P-017 | P1 | positive | **Повторное открытие закрытого (без merge) PR** | PR закрыт без merge | 1. Reopen | Статус снова Open | нет |
| TC-P-020 | P2 | negative | **Попытка создать PR без diff** | Ветка `feature-1` идентична `main` | 1. Попытаться создать PR | Ошибка об отсутствии различий между ветками либо кнопка Create недоступна | нет |
| TC-P-021 | P2 | negative | **PR с конфликтом — merge недоступен** | В base- и compare-ветке изменена одна и та же строка одного файла | 1. Открыть PR | Gitea показывает конфликт, кнопка Merge недоступна/задизейблена | нет |
| TC-P-040 | P2 | permissions | **Юзер без write-доступа не может смерджить PR** | PR открыт; юзер B без write-доступа | 1. Залогиниться юзером B<br>2. Открыть PR | Кнопка Merge недоступна | нет |
| TC-P-041 | P2 | permissions | **Автор не может одобрить собственный PR** | PR открыт автором | 1. Открыть PR автором<br>2. Review | Approve недоступен автору | нет |
| TC-P-030 | P3 | boundary | **Reopen недоступен у смерженного PR** | PR смерджен (Merged) | 1. Открыть PR | Кнопка Reopen отсутствует/недоступна у PR со статусом Merged | нет |

## Трассируемость: кейс → автотест

Только автоматизированные кейсы.

| Кейс | Автотест |
|------|----------|
| TC-A-001 | `tests/test_auth.py::test_login_with_valid_creds` |
| TC-A-002 | `tests/test_auth.py::test_logout` |
| TC-A-010 | `tests/test_registration.py::test_register_with_valid_creds[unique_creds]` |
| TC-A-011 | `tests/test_auth.py::test_access_page_without_auth_is_denied` |
| TC-A-020 | `tests/test_auth.py::test_login_with_invalid_creds[invalid_password]` |
| TC-A-021 | `tests/test_auth.py::test_login_with_invalid_creds[non_exist_creds]` |
| TC-A-022 | `tests/test_registration.py::test_registration_with_taken_login_or_email[in_use_username]` |
| TC-A-023 | `tests/test_registration.py::test_registration_with_invalid_email_format[no_symbol]` |
| TC-A-024 | `tests/test_registration.py::test_registration_with_invalid_password[failed_confirm_pass]` |
| TC-A-025 | `tests/test_registration.py::test_registration_with_invalid_password[min_length_pass]` |
| TC-A-026 | `tests/test_registration.py::test_registration_with_invalid_password[max_length_pass]` |
| TC-A-027 | `tests/test_registration.py::test_register_with_valid_creds[minimum_password_length]` |
| TC-A-028 | `tests/test_registration.py::test_register_with_valid_creds[upper_limit_password]` |
| TC-A-036 | `tests/test_registration.py::test_registration_with_invalid_email_format[empty_value]` |
| TC-A-037 | `tests/test_registration.py::test_registration_with_invalid_email_format[no_domain]` |
| TC-A-038 | `tests/test_registration.py::test_registration_with_invalid_email_format[no_local]` |
| TC-A-039 | `tests/test_registration.py::test_register_with_valid_creds[upper_limit_email]` |
| TC-A-041 | `tests/test_registration.py::test_register_with_valid_creds[minimum_email_length]` |
| TC-A-032 | `tests/test_registration.py::test_registration_with_empty_value_in_fields[empty_username]` |
| TC-A-033 | `tests/test_registration.py::test_registration_with_invalid_characters_in_username` |
| TC-A-035 | `tests/test_registration.py::test_registration_with_empty_value_in_fields[empty_password]` |
| TC-A-040 | `tests/test_registration.py::test_registration_with_invalid_email_format[above_max]` |
| TC-A-034a | `tests/test_registration.py::test_register_with_valid_creds[minimum_username_length]` |
| TC-A-034b | `tests/test_registration.py::test_register_with_valid_creds[upper_limit_username]` |
| TC-A-034c | `tests/test_registration.py::test_registration_with_username_exceeding_max_length` |
| TC-A-030 | `tests/test_auth.py::test_login_with_empty_fields` |
| TC-A-031 | `tests/test_registration.py::test_registration_with_taken_login_or_email[in_use_email]` |
| TC-R-001 | `tests/test_repo.py::test_create_public_repo` |
| TC-R-010 | `tests/test_repo.py::test_public_repo_is_accessible_to_another_user` |
| TC-R-011 | `tests/test_repo.py::test_create_private_repo` |
| TC-R-012 | `tests/test_repo.py::test_private_repo_is_inaccessible_to_another_user` |
| TC-R-013 | `tests/test_repo.py::test_create_repo_with_readme_file` |
| TC-R-014 | `tests/test_repo.py::test_create_repo_with_gitignore_and_readme_file` |
| TC-R-015 | `tests/test_repo.py::test_create_repo_with_license_and_readme_file` |
| TC-R-016 | `tests/test_repo.py::test_create_repo_with_license_readme_and_gitignore_files` |
| TC-R-017 | `tests/test_repo.py::test_create_repo_default_branch[custom_branch]` |
| TC-R-018 | `tests/test_repo.py::test_create_repo_in_organization` |
| TC-R-020 | `tests/test_repo.py::test_name_validation_no_repo_create[empty_name]` |
| TC-R-021 | `tests/test_repo.py::test_create_repo_with_duplicate_name` |
| TC-R-022 | `tests/test_repo.py::test_name_validation_no_repo_create[with_double_dot]` |
| TC-R-023a | `tests/test_repo.py::test_name_validation[emoji]` |
| TC-R-023b | `tests/test_repo.py::test_name_validation_no_repo_create[emoji]` |
| TC-R-024 | `tests/test_repo.py::test_repo_create_without_creation_rights` |
| TC-R-030 | `tests/test_repo.py::test_name_validation[min]` |
| TC-R-031 | `tests/test_repo.py::test_name_validation[max]` |
| TC-R-032 | `tests/test_repo.py::test_name_validation[over_max_truncated]` |
| TC-R-033 | `tests/test_repo.py::test_name_validation[with_space]` |
| TC-R-034 | `tests/test_repo.py::test_name_validation[with_slash]` |
| TC-R-035 | `tests/test_repo.py::test_name_validation[*]` |
| TC-R-037 | `tests/test_repo.py::test_create_repo_default_branch[empty_field_in_default_branch_field]` |
| TC-R-040 | `tests/test_repo.py::test_create_repo_with_description` |
| TC-R-043 | `tests/test_repo.py::test_create_repo_with_default_branch_upper_limit_value` |
| TC-R-044 | `tests/test_repo.py::test_create_repo_with_value_exceeding_maximum_for_default_branch` |
| TC-R-045 | `tests/test_repo.py::test_trying_create_repo_with_exceeding_description_value` |
| TC-I-001 | `tests/test_issues.py::test_add_issue_with_minimal_data` |
| TC-I-002 | `tests/test_issues.py::test_switch_issue_status[closing]` |
| TC-I-010 | `tests/test_issues.py::test_add_issue_with_pinned_comment` |
| TC-I-011 | `tests/test_issues.py::test_switch_issue_status[reopen]` |
| TC-I-012a | `tests/test_issues.py::test_update_issue_title` |
| TC-I-012b | `tests/test_issues.py::test_update_issue_pinned_comment` |
| TC-I-013 | `tests/test_issues.py::test_adding_issue_label` |
| TC-I-014 | `tests/test_issues.py::test_removing_label_from_issue` |
| TC-I-015 | `tests/test_issues.py::test_adding_issue_assignee` |
| TC-I-016 | `tests/test_issues.py::test_issue_linking_with_milestone` |
| TC-I-017 | `tests/test_issues.py::test_adding_timeline_comment` |
| TC-I-018 | `tests/test_issues.py::test_update_timeline_comment` |
| TC-I-019 | `tests/test_issues.py::test_delete_timeline_comment[confirm_delete]` |
| TC-I-019b | `tests/test_issues.py::test_delete_timeline_comment[cancel_delete]` |
| TC-I-020 | `tests/test_issues.py::test_adding_timeline_comment_with_closed_issue_status` |
| TC-I-030 | `tests/test_issues.py::test_add_issue_with_empty_title` |
| TC-I-032 | `tests/test_issues.py::test_add_issue_with_disabled_has_issue_param_in_repo` |
| TC-I-033 | `tests/test_issues.py::test_adding_issue_with_max_length_title` |
| TC-I-036 | `tests/test_issues.py::test_creating_issue_with_label` |
| TC-I-037 | `tests/test_issues.py::test_creating_issue_with_assignee` |
| TC-I-038 | `tests/test_issues.py::test_creating_issue_with_milestone` |
| TC-I-040 | `tests/test_issues.py::test_trying_update_issue_title_and_pinned_comment_by_other_user` |
| TC-I-041 | `tests/test_issues.py::test_trying_close_issue_by_other_user` |
| TC-I-042 | `tests/test_issues.py::test_trying_update_and_delete_comment_by_other_user` |
| TC-I-043 | `tests/test_issues.py::test_adding_timeline_comment_in_repo_by_other_user` |
