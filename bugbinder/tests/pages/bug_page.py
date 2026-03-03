from .base_page import BasePage

class BugPage(BasePage):
    def create_bug(self, project_name, title, steps, env="dev", comment=""):
        self.page.get_by_role("link", name="bug_report Bug Issue").nth(1).click()
        self.page.locator("input.select-dropdown").first.click()
        self.page.locator("span").filter(has_text=project_name).click()
        self.page.get_by_text("Title").click()
        self.page.get_by_role("textbox", name="Title").fill(title)
        self.page.get_by_text("Steps to reproduce").click()
        self.page.get_by_role("textbox", name="Steps to reproduce").fill("\r\n".join(steps))
        self.page.get_by_text("Environment").click()
        self.page.get_by_role("textbox", name="Environment").fill(env)
        self.page.get_by_text("Comment", exact=True).click()
        self.page.get_by_role("textbox", name="Comment").fill(comment)
        self.page.get_by_text("Submit").click()

    def assign_bug(self, username):
        self.page.locator("select[id^='select-']").first.select_option(username, force=True)
        self.page.locator(".assign-btn").first.click()

    def solve_bug(self, message=""):
        self.open("/task/")
        solution_box = self.page.locator("textarea[id^='solution-']").first
        solution_box.click()
        solution_box.fill(message)
        self.page.locator(".submit").first.click()
        
