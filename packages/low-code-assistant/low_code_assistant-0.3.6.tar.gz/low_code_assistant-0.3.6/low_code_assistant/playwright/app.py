from playwright.sync_api import Page


class AppHelper:
    def __init__(self, page: Page) -> None:
        self.page = page

    @property
    def menu_item(self):
        return self.page.locator('div[role="listbox"] >> text=App')

    @property
    def dialog(self):
        # it seems like vue=v-dialog does not work
        return self.page.locator("_vue=v-card >> text=App >> .. >> ..")

    @property
    def insert_code(self):
        return self.page.locator('button:has-text("Insert code")')

    @property
    def preview(self):
        return self.page.locator('button:has-text("Preview")')

    def insert_object(self, name):
        self.page.locator(f'_vue=v-switch[label="{name}"]').click()
