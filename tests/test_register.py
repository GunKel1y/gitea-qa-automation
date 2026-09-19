from playwright.sync_api import Page, expect
from uuid import uuid4

from conftest import TEST_LOGIN

TEST_EMAIL = 'test-email-' + str(uuid4())[:20] + '@test.ru'
TEST_PASSWORD = str(uuid4())

REGISTER_FORM = "//div[@class='ui attached segment']/form[@action='/user/sign_up']/.."

def test_register_with_truth_creds(page: Page, register_page):
    expect(page.locator(REGISTER_FORM)).to_be_visible()

    username_field = page.locator('#user_name')
    username_field.fill(TEST_LOGIN)
    expect(username_field).to_have_value(TEST_LOGIN)

    email_field = page.locator('#email')
    email_field.fill(TEST_EMAIL)
    expect(email_field).to_have_value(TEST_EMAIL)

    password_field = page.locator('#password')
    password_field.fill(TEST_PASSWORD)
    expect(password_field).to_have_value(TEST_PASSWORD)

    doublecheck_password_field = page.locator('#retype')
    doublecheck_password_field.fill(TEST_PASSWORD)
    expect(doublecheck_password_field).to_have_value(TEST_PASSWORD)

    register_button = page.get_by_text('Регистрация аккаунта')
    register_button.click()

    positive_register_banner = page.locator('div.positive.message')
    expect(positive_register_banner).to_be_visible()
    expect(positive_register_banner).to_have_text('Учётная запись успешно создана. Добро пожаловать!')

    expect(page).to_have_url('http://localhost:3000/')

