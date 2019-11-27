import pickle

from selenium import webdriver
from selenium.common.exceptions import InvalidCookieDomainException

from gacollector.settings.constants import GA_COOKE_PATH


class CookieKeeper:
    def __init__(self, browser: webdriver.Firefox, file_path=GA_COOKE_PATH):
        self.__browser__ = browser
        self.__file_path__ = file_path

    def save_cookies(self):
        with open(self.__file_path__, 'wb') as file:
            pickle.dump(self.__browser__.get_cookies(), file)

    def load_cookies(self):
        cookies = None
        try:
            with open(self.__file_path__, 'rb') as file:
                cookies = pickle.load(file)
                for cookie in cookies:
                    self.__browser__.add_cookie(cookie)
                return True
        except (EOFError, FileNotFoundError) as ex:
            print("Cookie не найдены")
            return False
        except InvalidCookieDomainException as ex:
            print(cookies)
            raise ex
