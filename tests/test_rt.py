
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

from settings import *
from pages.auth_page import AuthPage
from selenium.webdriver import Keys  # нажатие enter, tab
import time

driver = webdriver.Chrome()


def test_auth_form(selenium):
    driver.get(base_url)
    time.sleep(5)
    assert driver.find_element(By.NAME, 'password').is_displayed()


# Этот тест падает, если появляется captcha
def test_tab_active(selenium):
    """Проверяем, что при вводе номера телефона/почты/логина/лицевого счета -
    таб выбора аутентификации меняется автоматически"""
    page = AuthPage(selenium)
    time.sleep(3)
    # проверка, что по умолчанию активирован таб телефон
    assert 'active' in page.tab_phone.get_attribute('class')

    page.enter_user_name(email_valid)
    time.sleep(3)
    page.enter_user_name(Keys.TAB)
    # проверка, что таб почта стал активным после ввода email
    assert 'active' in page.tab_email.get_attribute('class')

    page.enter_user_name(Keys.CONTROL + "a" + Keys.DELETE)
    page.enter_user_name(login_valid)
    time.sleep(3)
    page.enter_user_name(Keys.TAB)
    # проверка, что таб логин стал активным после ввода логина
    assert 'active' in page.tab_login.get_attribute('class')

    page.enter_user_name(Keys.CONTROL + "a" + Keys.DELETE)
    page.enter_user_name(ls_valid)
    time.sleep(3)
    page.enter_user_name(Keys.TAB)
    # проверка, что таб лицевой счет стал активным после ввода лицевого счета
    assert 'active' in page.tab_ls.get_attribute('class')

    page.tab_email.click()
    page.user_name.send_keys(Keys.CONTROL + "a" + Keys.DELETE)
    page.user_name.send_keys(phone_number_valid)
    time.sleep(3)
    page.user_name.send_keys(Keys.TAB)
    #  проверка, что таб телефон стал активным после ввода телефона
    assert 'active' in page.tab_phone.get_attribute('class')
    print('\n', page.tab_login.get_attribute('class'))


'''Сценарий авторизации клиента по номеру телефона, кнопка "Телефон"'''


def test_auth_tel_valid(selenium):
    """Авторизация пользователя с валидными данными: номер телефона + пароль"""
    page = AuthPage(selenium)
    time.sleep(5)  # нужно задавать ожидание
    page.enter_user_name(phone_number_valid)
    page.enter_password(password_valid)
    time.sleep(2)  # Ввести captcha в идеале ее нужно обойти
    page.btn_click()
    time.sleep(5)
    element = selenium.find_element(By.TAG_NAME, 'h2').text

    # Проверяем переход на страницу личного кабинета
    assert page.get_relative_link() == '/account_b2c/page'
    # Проверяем личные данные пользователя в личном кабинете
    assert selenium.find_element(By.TAG_NAME, 'h2').text == f'{user["last_name"]}\n{user["name"]} {user["patronymic"]}'
    assert user['name'] or user['last_name'] in element


def test_auth_tel_invalid(selenium):
    """Проверяем, что авторизация пользователя с невалидным номером телефона невозможна"""
    page = AuthPage(selenium)
    time.sleep(5)  # нужно задавать ожидание
    page.enter_user_name(phone_number_invalid_list[0])
    page.enter_password(password_valid)
    time.sleep(2)  # Ввести captcha в идеале ее нужно обойти
    page.btn_click()
    time.sleep(1)
    element = selenium.find_element(By.XPATH, "//span[contains(text(),'Неверный формат телефона')]")

    # Проверяем, что на странице появляется предупреждение о неверном формате телефона
    assert element.text == "Неверный формат телефона"


@pytest.mark.parametrize("phone", phone_number_invalid_list)
def test_auth_phone_format(selenium, phone):
    """ Убедимся, что система проверяет формат введенного телефона и
    выводит сообщение если формат неверный"""
    page = AuthPage(selenium)
    page.user_name.send_keys(phone)
    page.user_name.send_keys(Keys.TAB)
    time.sleep(1)

    # Проверяем, что на странице появляется предупреждение о неверном формате телефона
    element = selenium.find_element(By.XPATH, "//span[contains(text(),'Неверный формат телефона')]")
    assert element.text == "Неверный формат телефона"


def ids_phone(val):
    return "phone: {0}".format(str(val))


def ids_password(val):
    return "password: {0}".format(str(val))


# Captcha мешает полноценно организовать проверку
@pytest.mark.parametrize("phone", phone_number_invalid_list, ids=ids_phone)
@pytest.mark.parametrize("password", password_invalid_list, ids=ids_password)
def test_multiply_phone(phone, password):
    """Набор негативных тестов невалидный номер телефона + невалидный пароль"""
    print("phone: {0}, password: {1}".format(phone, password))
    driver.get(base_url)
    time.sleep(5)  # нужно задавать ожидание
    driver.find_element(By.ID, 'username').send_keys(phone)
    driver.find_element(By.ID, 'password').send_keys(password)
    time.sleep(2)  # Ввести captcha в идеале ее нужно обойти
    driver.find_element(By.ID, 'kc-login').click()
    time.sleep(1)

    # Проверяем, что на странице появляется предупреждение о неверном формате телефона
    element = driver.find_element(By.XPATH, "//span[contains(text(),'Неверный формат телефона')]")
    assert element.text == "Неверный формат телефона"


'''Сценарий авторизации клиента по email, кнопка "Почта"'''


def test_auth_email_valid(selenium):
    """Авторизация пользователя с валидными данными: email + пароль"""
    page = AuthPage(selenium)
    time.sleep(5)
    page.tab_email.click()
    page.enter_user_name(email_valid)
    page.enter_password(password_valid)
    time.sleep(2)
    page.btn_click()
    time.sleep(5)
    element = selenium.find_element(By.TAG_NAME, 'h2').text

    # Проверяем переход на страницу личного кабинета
    assert page.get_relative_link() == '/account_b2c/page'
    # Проверяем личные данные пользователя в личном кабинете
    assert selenium.find_element(By.TAG_NAME, 'h2').text == f'{user["last_name"]}\n{user["name"]} {user["patronymic"]}'
    assert user['name'] or user['last_name'] in element


def test_auth_email_invalid(selenium):
    """Проверяем, что авторизация пользователя с невалидным email невозможна"""
    page = AuthPage(selenium)
    time.sleep(5)
    page.tab_email.click()
    page.enter_user_name(email_invalid_list[0])
    page.enter_password(password_valid)
    time.sleep(2)
    page.btn_click()
    time.sleep(5)
    element_btn = selenium.find_element(By.ID, 'forgot_password')
    attention = selenium.find_element(By.XPATH, "//span[contains(text(),'Неверный логин или пароль')]")

    # проверка, что надпись "Забыл пароль" меняет цвет
    assert 'animated' in element_btn.get_attribute('class')
    # проверка, что появляется сообщение "Неверный логин или пароль"
    assert attention.is_displayed()


def ids_email(val):
    return "email: {0}".format(str(val))


# Captcha мешает полноценно организовать проверку
@pytest.mark.parametrize("email", email_invalid_list, ids=ids_email)
@pytest.mark.parametrize("password", password_invalid_list, ids=ids_password)
def test_multiply_email(email, password):
    """Набор негативных тестов невалидный email + невалидный пароль"""
    print("phone: {0}, password: {1}".format(email, password))
    driver.get(base_url)
    time.sleep(5)  # нужно задавать ожидание
    driver.find_element(By.ID, 'username').send_keys(email)
    driver.find_element(By.ID, 'password').send_keys(password)
    time.sleep(2)  # Ввести captcha в идеале ее нужно обойти
    driver.find_element(By.ID, 'kc-login').click()
    time.sleep(1)
    element_btn = driver.find_element(By.ID, 'forgot_password')
    attention = driver.find_element(By.XPATH, "//span[contains(text(),'Неверный логин или пароль')]")

    # Проверяем, что надпись "Забыл пароль" меняет цвет
    assert 'animated' in element_btn.get_attribute('class')
    # Проверяем, что появляется сообщение "Неверный логин или пароль"
    assert attention.is_displayed()


'''Сценарий авторизации клиента по логину, кнопка "Логин":'''


def test_auth_login_valid(selenium):
    """Авторизация пользователя с валидными данными: логин + пароль"""
    page = AuthPage(selenium)
    time.sleep(5)
    page.tab_login.click()
    page.enter_user_name(login_valid)
    page.enter_password(password_valid)
    time.sleep(3)

    # "Запомнить меня" работает если нет captcha, как поймать если captcha?
    selenium.find_element(By.CSS_SELECTOR,
                          'section#page-right > div > div > div > form > div:nth-of-type(3) > label > span').click()
    time.sleep(1)
    page.btn_click()
    time.sleep(5)

    # Проверяем, что редирект на страницу личный кабинет произошел
    assert '/account_b2c/page' in page.get_relative_link()
    # Проверяем личные данные пользователя в личном кабинете
    assert selenium.find_element(By.TAG_NAME, 'h2').text == f'{user["last_name"]}\n{user["name"]} {user["patronymic"]}'


def test_auth_login_invalid(selenium):
    """Проверяем, что авторизация пользователя с невалидным логином невозможна"""
    page = AuthPage(selenium)
    time.sleep(5)
    page.tab_login.click()
    page.enter_user_name(login_invalid_list[0])
    page.enter_password(password_valid)
    time.sleep(3)

    # "Запомнить меня" работает если нет captcha, как поймать если captcha?
    selenium.find_element(By.CSS_SELECTOR,
                          'section#page-right > div > div > div > form > div:nth-of-type(3) > label > span').click()
    time.sleep(1)
    page.btn_click()
    time.sleep(1)
    attention = selenium.find_element(By.XPATH, "//span[contains(text(),'Неверный логин или пароль')]")

    # Проверяем, что на странице появилось предупреждение "Неверный логин или пароль"
    assert attention.is_displayed()
    # Проверяем, что редирект на страницу личный кабинет не произошел
    assert '/account_b2c/page' not in page.get_relative_link()


def ids_ls(val):
    return "email: {0}".format(str(val))


# Captcha мешает полноценно организовать проверку
@pytest.mark.parametrize("ls", email_invalid_list, ids=ids_ls)
@pytest.mark.parametrize("password", password_invalid_list, ids=ids_password)
def test_multiply_email(ls, password):
    """Набор негативных тестов невалидный логин + невалидный пароль"""
    print("phone: {0}, password: {1}".format(ls, password))
    driver.get(base_url)
    time.sleep(5)  # нужно задавать ожидание
    driver.find_element(By.ID, 'username').send_keys(ls)
    driver.find_element(By.ID, 'password').send_keys(password)
    time.sleep(2)  # Ввести captcha в идеале ее нужно обойти
    driver.find_element(By.ID, 'kc-login').click()
    time.sleep(1)
    element_btn = driver.find_element(By.ID, 'forgot_password')
    attention = driver.find_element(By.XPATH, "//span[contains(text(),'Неверный логин или пароль')]")

    # Проверяем, что надпись "Забыл пароль" меняет цвет
    assert 'animated' in element_btn.get_attribute('class')
    # Проверяем, что появляется сообщение "Неверный логин или пароль"
    assert attention.is_displayed()


'''Сценарий авторизации клиента по номеру лицевого счета, кнопка "Лицевой счет":'''
"""Нет тестового лицевого счета для проверки этого теста X-Fail"""


def test_login_ls(selenium):
    """Авторизация пользователя с валидными данными: логин + пароль"""
    page = AuthPage(selenium)
    time.sleep(5)
    page.tab_login.click()
    page.enter_user_name(login_valid)
    page.enter_password(password_valid)
    time.sleep(2)
    selenium.find_element(By.CSS_SELECTOR,
                          'section#page-right > div > div > div > form > div:nth-of-type(3) > label > span').click()
    time.sleep(1)
    page.btn_click()
    time.sleep(5)

    # Проверяем, что редирект на страницу личный кабинет произошел
    assert '/account_b2c/page' in page.get_relative_link()
    # Проверяем личные данные пользователя в личном кабинете
    assert selenium.find_element(By.TAG_NAME, 'h2').text == f'{user["last_name"]}\n{user["name"]} {user["patronymic"]}'


def test_login_ls_invalid():
    """Проверяем, что авторизация пользователя с невалидным логином невозможна"""
    driver.get("https://b2c.passport.rt.ru/")  # Запускает браузер
    time.sleep(5)
    driver.find_element(By.ID, 't-btn-tab-ls').click()  # Выбираем таб логин
    driver.find_element(By.ID, 'username').send_keys(login_invalid_list[0])
    driver.find_element(By.ID, 'password').send_keys(password_valid)
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR,
                        'section#page-right > div > div > div > form > div:nth-of-type(3) > label > span').click()
    time.sleep(1)
    driver.find_element(By.ID, 'kc-login').click()
    time.sleep(5)


# Тест упадет если на странице авторизации будет captcha
def test_auth_invalid():
    """Проверяем, что при некорректном вводе связки Номер + Пароль, выводится сообщение "Неверный логин или пароль" и
    элемент "Забыл пароль" перекрашивается в оранжевый цвет"""
    driver.get(base_url)
    time.sleep(5)
    driver.find_element(By.ID, 't-btn-tab-phone').click()  # Выбираем таб логин
    driver.find_element(By.ID, 'username').send_keys(phone_number_valid)
    driver.find_element(By.ID, 'password').send_keys(login_invalid_list[0])
    time.sleep(2)
    # try:
    #     driver.find_element(By.CLASS_NAME, 'rt-captcha__image').is_displayed()
    # except:
    #     return 'Captcha мешает завершить тест'

    driver.find_element(By.ID, 'kc-login').click()
    time.sleep(5)
    element_btn = driver.find_element(By.ID, 'forgot_password')
    attention = driver.find_element(By.XPATH, "//span[contains(text(),'Неверный логин или пароль')]")

    # проверка, что надпись "Забыл пароль" меняет цвет
    assert 'animated' in element_btn.get_attribute('class')
    # проверка, что появляется сообщение "Неверный логин или пароль"
    assert attention.is_displayed()
