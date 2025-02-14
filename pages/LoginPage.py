from pages.ProductPage import ProductPage


class LoginPage:
    def __init__(self, page):
        self.page = page
        self._username = page.locator("//input[@id='user-name']")
        self._password = page.locator("//input[@id='password']")
        self._btn_login = page.locator("//input[@id='login-button']")
        self._error_msg = page.locator("//div[contains(@class,'error')]/h3")

    def enter_username(self, username):
        self._username.fill(username)

    def enter_password(self, password):
        self._password.fill(password)

    def click_login_btn(self):
        self._btn_login.click()

    def do_login(self, username, password):
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_btn()
        # return ProductPage(self.page)

    @property
    def msg_error(self):
        return self._error_msg

    @property
    def login_button(self):
        return self._btn_login
