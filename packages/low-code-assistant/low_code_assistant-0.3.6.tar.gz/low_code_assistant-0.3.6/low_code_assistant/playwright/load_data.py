from playwright.sync_api import Page


class LoadDataHelper:
    def __init__(self, page: Page) -> None:
        self.page = page

    @property
    def menu_item(self):
        return self.page.locator('div[role="listbox"] >> text=Load data')

    @property
    def dialog(self):
        # it seems like vue=v-dialog does not work
        return self.page.locator("_vue=v-card >> text=Load data >> .. >> ..")

    @property
    def project_files(self):
        return ProjectFileHelper(self.page, self)

    @property
    def insert_code(self):
        return self.dialog.locator("text=Insert Code")


class ProjectFileHelper:
    def __init__(self, page: Page, load_data: LoadDataHelper) -> None:
        self.page = page
        self.load_data = load_data

    @property
    def tab_item(self):
        return self.load_data.dialog.locator("text=Project Files")

    @property
    def file_browser(self):
        return self.load_data.dialog.locator(".solara-file-browser")
