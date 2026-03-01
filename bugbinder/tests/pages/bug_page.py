from .base_page import BasePage

class BugPage(BasePage):

    def open_create(self):
        super().open("/bugs/create/")

    def create_bug(self, title, description):
        self.page.fill("input[name='title']", title)
        self.page.fill("textarea[name='description']", description)
        self.page.click("button[type='submit']")

    def assign_bug(self, user_id):
        self.page.select_option("select[name='assigned_to']", str(user_id))
        self.page.click("button[type='submit']")
    