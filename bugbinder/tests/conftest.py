import pytest

@pytest.fixture(autouse=True)
def clean_browser_context(context):
    context.clear_cookies()
    yield