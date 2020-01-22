import time

from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException, ElementNotInteractableException
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Import selector enums
from gacollector.selen.cookie_keeper import CookieKeeper
from gacollector.selen.page_selectors import GAPage
from gacollector.settings.constants import GECKO_DRIVER_PATH, GECKO_DRIVER_LOG_PATH, FIREFOX_BINARY_PATH


class BrowserScenario:

    def __init__(self, download_dir, profile_path: str, is_authorization_needed=True):
        self.download_dir = download_dir
        self.is_authorization_needed = is_authorization_needed
        self.profile_path = profile_path

        self.browser = None
        self.cookie = None

    def run_browser(self):
        # fp = webdriver.FirefoxProfile(self.profile_path)
        # fp.set_preference('browser.download.folderList', 2)
        # fp.set_preference('browser.download.manager.showWhenStarting', False)
        # fp.set_preference('browser.download.dir', self.download_dir)
        # fp.set_preference('browser.download.useDownloadDir', True)
        # fp.set_preference('browser.helperApps.neverAsk.saveToDisk',
        #                   'text/plain, application/vnd.ms-excel, text/csv, text/comma-separated-values, '
        #                   'application/octet-stream, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        # fp.update_preferences()
        #
        # caps = DesiredCapabilities.FIREFOX.copy()
        # caps["firefox_profile"] = fp.encoded
        # caps["marionette"] = True
        # self.browser = webdriver.Firefox(firefox_profile=fp, firefox_binary=FIREFOX_BINARY_PATH,
        #                                  capabilities=caps,
        #                                  executable_path=GECKO_DRIVER_PATH, service_log_path=GECKO_DRIVER_LOG_PATH)
        opts = webdriver.chrome.options.Options()
        opts.add_argument(f"user-data-dir={self.profile_path}")
        from selenium.webdriver.chrome.service import Service

        service = Service(GECKO_DRIVER_PATH)
        service.start()
        driver = webdriver.Remote(service.service_url)
        time.sleep(5) # Let the user actually see something!

        self.browser = webdriver.Chrome(executable_path=GECKO_DRIVER_PATH, chrome_options=opts,)
        self.browser.implicitly_wait(10)
        self.browser.set_script_timeout(10)

        self.cookie = CookieKeeper(self.browser)
        if self.is_authorization_needed:

            self.browser.get("https://myaccount.google.com")
            if not self.cookie.load_cookies():
                self.browser.get("https://accounts.google.com/signin/v2")
                input("Войдите на сайт и нажмите enter:")
                if self.browser.current_url not in ['https://myaccount.google.com/intro',
                                                    'https://myaccount.google.com']:
                    self.browser.get("https://myaccount.google.com")
                self.cookie.save_cookies()
            else:
                print("Куки успешно загрузились!")
                # TODO check cookie expire
            self.is_authorization_needed = False
        self.cookie.load_cookies()

    def __wait_for(self, target_css, timeout=60):
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
            self.__click_and_wait(GAPage.btn_export, GAPage.choice_to_csv)
            self.__click_and_wait(GAPage.choice_to_csv, GAPage.anchor_loaded)
        except (TimeoutException, StaleElementReferenceException, ElementNotInteractableException):
            # TODO refactoring method
            if count is None:
                count = 0

            if count >= 2:
                print("Something is wrong third try save csv")
                time.sleep(5)
            if count >= 3:
                input("Получил ошибку при попытке скачать csv")

            count += 1
            self.__get_page_data(count=count)

    def __browse_next_page(self):
        pagination_text = self.browser.find_element_by_css_selector(GAPage.pagination_nums).text
        pagination_text = pagination_text.split(" ")
        if pagination_text[2] == pagination_text[4]:
            return False
        self.__click_and_wait(GAPage.anchor_nex_page, GAPage.anchor_loaded, 15)
        # TODO return true (?)

    def get_week_data(self, url):
        self.browser.get(url)
        while True:
            self.__wait_for(GAPage.main_frame, 60)
            self.browser.switch_to_frame(self.browser.find_element_by_id(GAPage.main_frame_ID))
            self.__wait_while_visible(GAPage.alert_loading_ID)
            self.__get_page_data()
            self.__wait_while_visible(GAPage.alert_download_ID)
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
