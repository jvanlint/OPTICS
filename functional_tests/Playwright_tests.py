from playwright.sync_api import Page
import pytest


@pytest.mark.skip
def test_example_is_working(page):
    page.goto("https://example.com")
    assert page.inner_text("h1") == "Example Domain"
    page.click("text=More information")
