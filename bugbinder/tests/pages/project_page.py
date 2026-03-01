from .base_page import BasePage

class ProjectPage(BasePage):

    def open_create(self):
        super().open("/projects/create/")

    def create_project(self, name, description):
        self.page.fill("input[name='name']", name)
        self.page.fill("textarea[name='description']", description)
        self.page.click("button[type='submit']")
    