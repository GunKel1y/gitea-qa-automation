import os

from playwright.sync_api import Page, expect


def test_login_with_valid_creds(page: Page, register_person_for_auth):
    person_login = register_person_for_auth[0]
    person_pass = register_person_for_auth[1]

    auth_form = page.locator("//div[@class='ui attached segment']/form[@action='/user/login']/..")
    expect(auth_form).to_be_visible()

    username_field = page.locator("input#user_name")
    username_field.fill(person_login)
    expect(username_field).to_have_value(person_login)

    password_field = page.locator("input#password")
    password_field.fill(person_pass)
    expect(password_field).to_have_value(person_pass)

    login_button = page.locator('button.ui.primary.button')
    login_button.click()

    expect(page).to_have_url(f'{os.getenv("BASE_URL_UI")}/')

    dashboard = page.locator("div.dashboard[role='main']")
    expect(dashboard).to_be_visible()