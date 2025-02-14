from datetime import datetime
from pathlib import Path
import pytest
import json
import configparser
import os
import shutil
from playwright.sync_api import Page, Playwright


# data from test_config.ini file
@pytest.fixture(scope="session")
def config_data():
    config = configparser.ConfigParser()
    config.read(Path(__file__).parent / 'config' / 'test_config.ini')
    return config['default']


# data from test_data.json file
@pytest.fixture(scope="session")
def test_data():
    with open(Path(__file__).parent / 'config' / 'test_data.json') as f:
        data = json.load(f)
    return data


@pytest.fixture(scope="session")
def browser_context_args(config_data):
    return {
        "headless": config_data.getboolean('headless'),
        "slow_mo": config_data.getint('slow_mo'),
    }


@pytest.fixture(scope="session")
def browser(playwright: Playwright, config_data, browser_context_args):
    browser_name = config_data['browser']
    browser = getattr(playwright, browser_name).launch(**browser_context_args)
    yield browser
    browser.close()


@pytest.fixture
def page_setup_teardown(browser, config_data):
    # context = browser.new_context(record_video_dir='videos')
    context = browser.new_context()
    page = context.new_page()
    page.goto(config_data['base_url'])
    yield page
    context.close()


# page fixture for set up and tear down
@pytest.fixture
def set_up_tear_down(page: Page, config_data):
    print("Page about to navigate")
    # page.goto("https://www.saucedemo.com/")
    page.goto(config_data['base_url'])
    print("base url --->", config_data['base_url'])
    yield page
    print("Page Closed")


# browser fixture for set up and tear down
@pytest.fixture
def set_up_tear_down_browser(playwright: Playwright, config_data):
    browser_name = config_data['browser']
    browser = getattr(playwright, browser_name).launch(
        headless=config_data.getboolean('headless'),
        slow_mo=config_data.getint('slow_mo')
    )
    context = browser.new_context()
    page = context.new_page()
    page.goto(config_data['base_url'])

    yield page

    context.close()
    browser.close()


# clearing previous reports
def clear_directory(directory_path):
    if os.path.exists(directory_path):
        shutil.rmtree(directory_path)
    os.makedirs(directory_path)


@pytest.fixture(scope='session', autouse=True)
def clear_previous_reports_and_artifacts():
    clear_directory('reports')
    print("Cleared previous reports")
    clear_directory('screenshots')
    print("Cleared previous screenshots")
    clear_directory('videos')
    print("Cleared previous videos")


# report generation
@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    # set custom options only if none are provided from command line
    if not config.option.htmlpath:
        now = datetime.now()
        # create report target dir
        reports_dir = Path('reports')
        reports_dir.mkdir(parents=True, exist_ok=True)
        # custom report file
        report = reports_dir / f"report_{now.strftime('%Y_%m-%d_%H%M')}.html"
        # adjust plugin options
        config.option.htmlpath = report
        config.option.self_contained_html = True


# capture screenshots on failure
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == 'call' and rep.failed:
        # if you are using only page fixture without using browser launch and no need of videos
        # if 'set_up_tear_down' in item.fixturenames:
        #     page = item.funcargs['set_up_tear_down']
        if 'page_setup_teardown' in item.fixturenames:
            page = item.funcargs['page_setup_teardown']
            screenshot_dir = Path('screenshots')
            screenshot_dir.mkdir(parents=True, exist_ok=True)
            screenshot_path = screenshot_dir / f"{rep.nodeid.replace('::', '_')}.png"
            page.screenshot(path=str(screenshot_path))

            print(f"Screenshot saved to {screenshot_path}")

