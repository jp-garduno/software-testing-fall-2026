from behave import given, when, then
from selenium.webdriver.common.by import By

@given('I am on google page')
def on_google(context):
    context.browser.get('https://www.google.com/')

@when('I enter valorant in the search bar')
def search_valorant(context):
    context.browser.find_element(By.XPATH, '//*[@id="ti6dpd"]').send_keys('Valorant')

@then('I see the dashboard')
def step_impl(context):
    assert 'Dashboard' in context.browser.title