from .base_page import BasePage

class ProjectPage(BasePage):
    def create_project(self, name, description):
        self.page.get_by_role("link", name="Add Project").click()
        self.page.get_by_text("Project Name").click()
        self.page.get_by_role("textbox", name="Project Name").fill(name)
        self.page.get_by_text("Description").click()
        self.page.get_by_role("textbox", name="Description").fill(description)
        self.page.get_by_role("button", name="Create Project").click()

    def add_member(self, username):
        self.page.locator(".box.dev-wraper > .box-head > .modal-trigger").click()
        self.page.get_by_text("Email or Username").click()
        self.page.get_by_role("textbox", name="Email or Username").fill(username)
        self.page.get_by_text("Search").click()
        self.page.locator("#save-dev").click()
