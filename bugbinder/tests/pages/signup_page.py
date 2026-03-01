import time

from .base_page import BasePage

class SignupPage(BasePage):
    def signup(self, username, email, password):
        # Sign up a new user
        self.page.locator("#nav-mobile").get_by_role("link", name="local_hospital Sign up").click()
        self.page.get_by_text("Username").click()
        self.page.get_by_role("textbox", name="Username").click()
        self.page.get_by_role("textbox", name="Username").fill(username)
        self.page.locator("#modal2").get_by_text("Email Address").click()
        self.page.get_by_role("textbox", name="Email Address").fill(email)
        self.page.locator("#modal2").get_by_text("Password", exact=True).click()
        self.page.get_by_role("textbox", name="Password").fill(password)
        self.page.locator("#signup-btn").click()
        time.sleep(5)  # Wait for the page to load after signing up

    def fill_additional_details(self, full_name, mobile_number, organization, github_username, linkedin_username):
        self.page.get_by_role("link", name="account_circle test_user").nth(1).click()
        self.page.locator("#edit-btn").click()
        self.page.get_by_role("textbox", name="Full Name").click()
        self.page.get_by_role("textbox", name="Full Name").fill(full_name)
        self.page.get_by_role("textbox", name="Mobile Number").click()
        self.page.get_by_role("textbox", name="Mobile Number").fill(mobile_number)
        self.page.get_by_role("textbox", name="Organization").click()
        self.page.get_by_role("textbox", name="Organization").fill(organization)
        self.page.get_by_role("textbox", name="GitHub username").click()
        self.page.get_by_role("textbox", name="GitHub username").fill(github_username)
        self.page.get_by_role("textbox", name="Linkedin username").click()
        self.page.get_by_role("textbox", name="Linkedin username").fill(linkedin_username)
        self.page.locator("#save-btn").click()