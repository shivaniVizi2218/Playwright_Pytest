from playwright.sync_api import expect
from pages.LoginPage import LoginPage
from pages.ProductPage import ProductPage


def test_valid_login(page_setup_teardown, config_data):
    page = page_setup_teardown
    # page = set_up_tear_down_browser
    print("Test Valid  Login begins")
    login_page = LoginPage(page)
    product_page = ProductPage(page)
    username = config_data['username']
    password = config_data['password']
    # product_page = login_page.do_login(username="standard_user", password="secret_sauce")
    # login_page.do_login(username="standard_user", password="secret_sauce")
    login_page.do_login(username=username, password=password)
    expect(product_page.products_header).to_be_visible()
    print("Test Valid Login Ended")


def test_invalid_login(page_setup_teardown, test_data):
    page = page_setup_teardown
    # page = set_up_tear_down_browser
    print("Test Invalid Login begins")
    login_page = LoginPage(page)
    product_page = ProductPage(page)
    username = test_data['invalid_login']['username']
    password = test_data['invalid_login']['password']
    print("invalid username -->", username, "& invalid password -->", password)
    login_page.do_login(username=username, password=password)
    # login_page.do_login(username="invalid_user", password="secret_sauce")
    expect(product_page.products_header).not_to_be_visible()
    expect(login_page.msg_error).to_be_visible()
    expect(login_page.msg_error).to_contain_text(test_data['login_error_msg']['invalid_login'],
                                                 ignore_case=True)
    print("Test Invalid Login Ended")


def test_logout(page_setup_teardown, config_data):
    page = page_setup_teardown
    print("Test Logout Begins")
    login_page = LoginPage(page)
    product_page = ProductPage(page)
    username = config_data['username']
    password = config_data['password']
    # login_page.do_login(username="standard_user", password="secret_sauce")
    login_page.do_login(username=username, password=password)
    expect(product_page.products_header).to_have_text("Products")
    product_page.do_logout()
    expect(login_page.login_button).to_be_visible()
    print("Test Logout Ended")


def test_access_page_without_login(page_setup_teardown, config_data, test_data):
    page = page_setup_teardown
    print("Test Access without Login Begins")
    login_page = LoginPage(page)
    product_page = ProductPage(page)
    username = config_data['username']
    password = config_data['password']
    # login_page.do_login(username="standard_user", password="secret_sauce")
    login_page.do_login(username=username, password=password)
    print("Logged in")
    current_url = page.url
    print("current url ----->", current_url)
    print("Got URL")
    product_page.do_logout()
    print("Logged out")
    page.goto(current_url)
    expect(login_page.msg_error).to_be_visible()
    expect(login_page.msg_error).to_contain_text(test_data['login_error_msg']['access_without_login'],
                                                 ignore_case=True)
    print("Test Access without Login Ended")


def test_login_locked_out_user(page_setup_teardown, test_data):
    page = page_setup_teardown
    print("Test Login Locked_Out_User begins")
    login_page = LoginPage(page)
    product_page = ProductPage(page)
    username = test_data['locked_out_login']['username']
    password = test_data['locked_out_login']['password']
    print("locked_out_login username -->", username, "& locked_out_login pswd -->", password)
    login_page.do_login(username=username, password=password)
    # login_page.do_login(username="locked_out_user", password="secret_sauce")
    expect(product_page.products_header).to_be_visible()
    expect(login_page.msg_error).to_be_visible()
    expect(login_page.msg_error).to_contain_text(test_data['login_error_msg']['locked_out_login'],
                                                 ignore_case=True)
    print("Test Login Locked_Out_User Ended")


def test_empty_login(page_setup_teardown, test_data):
    # page = set_up_tear_down_browser
    page = page_setup_teardown
    print("Test Empty Login begins")
    login_page = LoginPage(page)
    login_page.click_login_btn()
    expect(login_page.msg_error).to_be_visible()
    expect(login_page.msg_error).not_to_contain_text(test_data['login_error_msg']['empty_login'],
                                                     ignore_case=True)
