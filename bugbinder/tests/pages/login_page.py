import time

from .base_page import BasePage

class LoginPage(BasePage):
    def login(self, username, password):
        self.page.locator("#nav-mobile").get_by_role("link", name="Login account_box").click()
        self.page.locator("#login").get_by_text("Email Address").click()
        self.page.get_by_role("textbox", name="Email Address").fill(username)
        self.page.locator("#login").get_by_text("Password", exact=True).click()
        self.page.get_by_role("textbox", name="Password").fill(password)
        self.page.locator("#login-btn").click()
        time.sleep(5)  # Wait for the page to load after login