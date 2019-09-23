# -*- coding: utf-8 -*
import pickle
import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, \
    StaleElementReferenceException, ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

browser = None


def run_browser(download_dir, is_first_time):
    global browser
    browser = webdriver.Firefox(executable_path='../selenium_drv/geckodriver.exe')
    browser.implicitly_wait(10)
    browser.set_script_timeout(10)
    if is_first_time:
        browser.get("https://accounts.google.com/signin/v2")
        input("Войдите на сайт и нажмите enter")
        save_cookies()
    load_cookies()


ANCHOR_LOADED = 'th.ACTION-sort'
ANCHOR_NEXT = "li.ACTION-paginate:nth-of-type(2)"


def save_cookies():
    pickle.dump(browser.get_cookies(), open("cookies.pkl", "wb"))


def load_cookies():
    cookies = pickle.load(open("cookies.pkl", "rb"))
    for cookie in cookies:
        browser.add_cookie(cookie)


def wait_for(target_css, timeout=15):
    wait = WebDriverWait(browser, timeout)
    return wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, target_css)))


def click_and_wait(target_css, waited_for_css, timeout=7):
    wait = WebDriverWait(browser, timeout)
    # wait.until_not(EC.presence_of_element_located((By.CLASS_NAME, "ID-loadingProgressBarScreen")))
    while True:
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, target_css))).click()
        except (ElementClickInterceptedException):
            time.sleep(1)
        else:
            break
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, waited_for_css)))


def get_page_data(count=None):
    try:
        click_and_wait(".ID-exportControlButton", "li.ACTION-export.TARGET-CSV")
        click_and_wait("li.ACTION-export.TARGET-CSV", ANCHOR_LOADED)
    except (TimeoutException, StaleElementReferenceException, ElementNotInteractableException):
        if count is None:
            count = 0

        if count >= 2:
            print("Something is wrong third try save csv")
            time.sleep(5)
        if count >= 3:
            input()

        count += 1
        get_page_data(count=count)


def browse_next_page():
    pagination_text = browser.find_element_by_css_selector("span.C_PAGINATION_ROWS_LONG>label").text
    pagination_text = pagination_text.split(" ")
    if pagination_text[2] == pagination_text[4]:
        return False
    click_and_wait(ANCHOR_NEXT, ANCHOR_LOADED, 15)


def wait_while_visible(_id, timeout=15):
    try:
        wait = WebDriverWait(browser, timeout)
        wait.until_not(EC.visibility_of_element_located((By.ID, _id)))
    except TimeoutException:
        pass


def get_week_data(url):
    browser.get(url)
    while True:
        wait_for("iframe#galaxyIframe")
        browser.switch_to_frame(browser.find_element_by_id("galaxyIframe"))
        wait_while_visible("ID-reportLoading")
        get_page_data()
        wait_while_visible("ID-messageBox")
        if not browse_next_page():
            break


def manage_weeks(urls, download_dir, is_first_time=False):
    run_browser(download_dir, is_first_time)
    for url in urls:
        get_week_data(url)
    browser.close()


def wait_cookies(download_dir):
    run_browser(download_dir, True)
    input("Нажмите enter, после авторизации")
    save_cookies()
    browser.close()


def _test(urls, download_dir):
    import os
    import shutil
    folder = os.path.join(os.getcwd(), "GA_test")
    c = 1
    # print(os.listdir(folder))
    print(folder)
    for file in os.listdir(folder):
        print("Copy file:", file, "\tto:", download_dir)
        shutil.copyfile(os.path.join(folder, file), os.path.join(download_dir, file))
        c += 1


if __name__ == '__main__':
    # log_in__google("analytics@delvepartners.com", "R]q(0Q7F?RvCF\-J")
    # save_cookies()
    # exit()
    browser.get("https://analytics.google.com")
    load_cookies()
    # manage_weeks()
