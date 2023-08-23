from pages.base import BasePage
from pages.locators import AuthLocators

import time, os


class AuthPage(BasePage):

    def __init__(self, driver, timeout=10):
        super().__init__(driver, timeout)
        url = os.getenv("LOGIN_URL") or "https://b2c.passport.rt.ru/"
        driver.get(url)
        self.user_name = driver.find_element(*AuthLocators.AUTH_USER_NAME)
        self.password = driver.find_element(*AuthLocators.AUTH_PASS)
        self.btn = driver.find_element(*AuthLocators.AUTH_BTN)
        self.tab_phone = driver.find_element(*AuthLocators.AUTH_TAB_PHONE)
        self.tab_email = driver.find_element(*AuthLocators.AUTH_TAB_EMAIL)
        self.tab_login = driver.find_element(*AuthLocators.AUTH_TAB_LOGIN)
        self.tab_ls = driver.find_element(*AuthLocators.AUTH_TAB_LS)
        # self.auth_phone_invalid = driver.find_element(*AuthLocators.AUTH_PHONE_INVALID) нет локатора и тест падает

        time.sleep(3)

    def enter_user_name(self, value):
        self.user_name.send_keys(value)

    def enter_password(self, value):
        self.password.send_keys(value)

    def btn_click(self):
        self.btn.click()
