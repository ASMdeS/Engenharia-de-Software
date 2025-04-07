from behave import given, when, then
from pages.Analysis_Company import is_valid_ticker

@given('o ticker "{ticker}"')
def step_given_ticker(context, ticker):
    context.ticker = ticker

@when('verifico se o ticker é válido')
def step_when_verify_ticker(context):
    context.result = is_valid_ticker(context.ticker)

@then('o resultado deve ser "{expected_result}"')
def step_then_check_result(context, expected_result):
    if expected_result == "válido":
        assert context.result is True
    else:
        assert context.result is False
