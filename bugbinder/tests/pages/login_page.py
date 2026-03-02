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

    def reset_password(self, old_password, new_password):
        self.page.get_by_role("link", name="account_circle test_user").nth(1).click()
        self.page.locator("#edit-btn").click()
        self.page.get_by_role("link", name="Change Password").click()
        self.page.get_by_text("Current Password").click()
        self.page.get_by_role("textbox", name="Current Password").fill(old_password)
        self.page.get_by_text("New Password").click()
        self.page.get_by_role("textbox", name="New Password").fill(new_password)
        self.page.get_by_text("Confirm Password").click()
        self.page.get_by_role("textbox", name="Confirm Password").fill(new_password)
        self.page.get_by_text("Save").click()
