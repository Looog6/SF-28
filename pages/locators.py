from selenium.webdriver.common.by import By


class RegLocators:
    REG_BTN = (By.NAME, 'register')
    REG_FIRST_NAME = (By.NAME, 'firstName')  # поле для ввода имени
    REG_LAST_NAME = (By.NAME, 'lastName')  # поле для ввода фамилии
    REG_PASS = (By.ID, 'password')  # поле для ввода пароля
    REG_PASS_CON = (By.ID, 'password-confirm')  # поле для подтверждения пароля

    # REG_ADDRESS = (By.ID, 'address')  # дропдаун выбрать регион
    # REG_LINK_UA1 = (By.XPATH, '//*[@id="page-right"]/div/div/div/form/div[5]/a')  # пользовательское соглашение
    # REG_LINK_COOKIE = (By.XPATH, '//*[@id="app-footer"]/div[1]/div[2]/span/span')  # Cookies
    # REG_LINK_CP = (By.XPATH, '//*[@id="rt-footer-agreement-link"]/span[1]')  # футер политика конфиденциальности
    # REG_LINK_UA2 = (By.XPATH, '//*[@id="rt-footer-agreement-link"]/span[2]')  # футер пользовательское соглашение
    # REG_LINK_PHONE = (By.XPATH, '//*[@id="app-footer"]/div[2]/a')  # телефон кликабелен


class AuthLocators:
    AUTH_USER_NAME = (By.ID, 'username')  # поле ввода email, телефон, логин или ЛС
    AUTH_PASS = (By.ID, 'password')  # поле ввода пароля
    AUTH_BTN = (By.ID, 'kc-login')  # кнопка авторизации
    AUTH_TAB_PHONE = (By.ID, 't-btn-tab-phone')  # таб телефон
    AUTH_TAB_EMAIL = (By.ID, 't-btn-tab-mail')  # таб почта
    AUTH_TAB_LOGIN = (By.ID, 't-btn-tab-login')  # таб логин
    AUTH_TAB_LS = (By.ID, 't-btn-tab-ls')  # таб лицевой счет

    # AUTH_PHONE_INVALID = (By.XPATH, "//span[contains(text(),'Неверный формат телефона')]")
    # AUTH_LINK_UA1 = (By.XPATH, '//*[@id="page-right"]/div/div/div/form/div[4]/a')  # пользовательское соглашение
    # AUTH_LINK_VK = (By.ID, 'oidc_vk')  # авторизация через социальную сеть VK
    # AUTH_LINK_OK = (By.ID, 'oidc_ok')  # авторизация через социальную сеть OK
    # AUTH_LINK_MAIL = (By.ID, 'oidc_mail')  # авторизация привязанным аккаунтом Mail
    # AUTH_LINK_YA = (By.ID, 'oidc_ya')  # авторизация привязанным аккаунтом Яндекс
    # AUTH_LINK_REG = (By.ID, 'kc-register')  # мое мнение это нужно для нового пользователя
    # AUTH_LINK_COOKIE = (By.XPATH, '//*[@id="app-footer"]/div[1]/div[2]/span/span')  # футер Cookies
    # AUTH_LINK_CP = (By.XPATH, '//*[@id="rt-footer-agreement-link"]/span[1]')  # футер политика конфиденциальности
    # AUTH_LINK_UA2 = (By.XPATH, '//*[@id="rt-footer-agreement-link"]/span[2]')  # футер пользовательское соглашение
    # AUTH_LINK_PHONE = (By.XPATH, '//*[@id="app-footer"]/div[2]/a') # телефон кликабелен

    # этот локатор рабочий если нет captcha
    # AUTH_BTN_MEM = (By.CSS_SELECTOR,
    # 'section#page-right > div > div > div > form > div:nth-of-type(3) > label > span')  # запомнить меня
