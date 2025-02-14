class ProductPage:
    def __init__(self, page):
        self.page = page
        self._header_products = page.locator("//span[@class='title']")
        self._btn_burger_menu = page.locator("//button[contains(@id,'burger-menu')]")
        self._btn_logout = page.locator("//a[text()='Logout']")

    @property
    def products_header(self):
        return self._header_products

    def click_burger_menu(self):
        self._btn_burger_menu.click()

    def click_logout(self):
        self._btn_logout.click()

    def do_logout(self):
        self.click_burger_menu()
        self.click_logout()
