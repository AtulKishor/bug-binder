class BasePage:
    def __init__(self, page, live_server):
        self.page = page
        self.base_url = live_server.url

    def open(self, path=""):
        self.page.goto(f"{self.base_url}{path}")

    def get_title(self):
        return self.page.title()
    
