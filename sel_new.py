# -*- coding: utf-8 -*
import pickle
import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, \
    StaleElementReferenceException, ElementNotInteractableException
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# css selectors
ANCHOR_LOADED = 'th.ACTION-sort'
ANCHOR_NEXT = "li.ACTION-paginate:nth-of-type(2)"
URL_GOOGLE = ''
URL_GOOGLE_LOGIN = 'https://accounts.google.com/signin/v2'


class CookieKeeper:
    __file_path__ = ''
    __browser__ = None

    def __init__(self, browser: webdriver.Firefox, file_path="cookies.pkl"):
        self.__browser__ = browser
        self.__file_path__ = file_path

    def save_cookies(self):
        with open(self.__file_path__, 'wb') as file:
            pickle.dump(self.__browser__.get_cookies(), file)

    def load_cookies(self):
        try:
            with open(self.__file_path__, 'rb') as file:
                cookies = pickle.load(file)
                for cookie in cookies:
                    from selenium.common.exceptions import InvalidCookieDomainException
                    try:
                        self.__browser__.add_cookie(cookie)
                    except InvalidCookieDomainException:
                        pass
        except (EOFError, FileNotFoundError) as ex:
            print("Cookie не найдены")


class BrowserScenario:
    __FIREFOX_BINARY_PATH__ = "C:/Program Files/Mozilla Firefox/firefox.exe"
    __GECKO_DRIVER_PATH__ = '../selenium_drv/geckodriver.exe'

    def __init__(self, download_dir, profile_path: str, is_authorization_needed=True):
        self.download_dir = download_dir
        self.is_authorization_needed = is_authorization_needed
        self.profile_path = profile_path

        self.browser = None
        self.cookie = None

    def run_browser(self):
        fp = webdriver.FirefoxProfile(self.profile_path)
        fp.set_preference('browser.download.folderList', 2)
        fp.set_preference('browser.download.manager.showWhenStarting', False)
        fp.set_preference('browser.download.dir', self.download_dir)
        fp.set_preference('browser.download.useDownloadDir', True)
        fp.set_preference('browser.helperApps.neverAsk.saveToDisk',
                          'text/plain, application/vnd.ms-excel, text/csv, text/comma-separated-values, '
                          'application/octet-stream, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        fp.update_preferences()

        caps = DesiredCapabilities.FIREFOX.copy()
        caps["firefox_profile"] = fp.encoded
        caps["marionette"] = True
        self.browser = webdriver.Firefox(firefox_profile=fp, firefox_binary=self.__FIREFOX_BINARY_PATH__,
                                         capabilities=caps,
                                         executable_path=self.__GECKO_DRIVER_PATH__)
        self.browser.implicitly_wait(10)
        self.browser.set_script_timeout(10)

        self.cookie = CookieKeeper(self.browser)
        if self.is_authorization_needed:
            self.browser.get(URL_GOOGLE_LOGIN)
            self.cookie.load_cookies()
            input("Войдите на сайт и нажмите enter (Возможно куки уже загрузились, попробуйте перезагрузить страницу)")
            self.browser.get(URL_GOOGLE_LOGIN)
            self.cookie.save_cookies()
            self.is_authorization_needed = False
        self.cookie.load_cookies()

    def __wait_for(self, target_css, timeout=15):
        wait = WebDriverWait(self.browser, timeout)
        return wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, target_css)))

    def __click_and_wait(self, target_css, waited_for_css, timeout=7):
        wait = WebDriverWait(self.browser, timeout)
        # wait.until_not(EC.presence_of_element_located((By.CLASS_NAME, "ID-loadingProgressBarScreen")))
        while True:
            try:
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, target_css))).click()
            except (ElementClickInterceptedException):
                time.sleep(1)
            else:
                break
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, waited_for_css)))

    def __wait_while_visible(self, _id, timeout=15):
        try:
            wait = WebDriverWait(self.browser, timeout)
            wait.until_not(EC.visibility_of_element_located((By.ID, _id)))
        except TimeoutException:
            pass

    def __get_page_data(self, count=None):
        try:
            self.__click_and_wait(".ID-exportControlButton", "li.ACTION-export.TARGET-CSV")
            self.__click_and_wait("li.ACTION-export.TARGET-CSV", ANCHOR_LOADED)
        except (TimeoutException, StaleElementReferenceException, ElementNotInteractableException):
            # TODO refactoring method
            if count is None:
                count = 0

            if count >= 2:
                print("Something is wrong third try save csv")
                time.sleep(5)
            if count >= 3:
                input()

            count += 1
            self.__get_page_data(count=count)

    def __browse_next_page(self):
        pagination_text = self.browser.find_element_by_css_selector("span.C_PAGINATION_ROWS_LONG>label").text
        pagination_text = pagination_text.split(" ")
        if pagination_text[2] == pagination_text[4]:
            return False
        self.__click_and_wait(ANCHOR_NEXT, ANCHOR_LOADED, 15)

    def get_week_data(self, url):
        self.browser.get(url)
        while True:
            self.__wait_for("iframe#galaxyIframe")
            self.browser.switch_to_frame(self.browser.find_element_by_id("galaxyIframe"))
            self.__wait_while_visible("ID-reportLoading")
            self.__get_page_data()
            self.__wait_while_visible("ID-messageBox")
            if not self.__browse_next_page():
                break

    def __enter__(self):
        # open browser
        self.run_browser()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # close browser
        self.browser.close()
        return False


if __name__ == '__main__':
    pass
