import pytest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from settings import *
from selenium.webdriver import Keys  # нажатие enter, tab
import time

from faker import Faker
fake = Faker()
fake_ru = Faker('ru_RU')

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 5)


def test_reg_format_name():
    """Проверим, что система проверяет формат введенного имени"""
    driver.get(base_url)
    wait.until(EC.element_to_be_clickable((By.ID, 'kc-register')))
    driver.find_element(By.ID, 'kc-register').click()
    driver.find_element(By.NAME, 'firstName').send_keys(user_name_invalid_list[1] + Keys.TAB)

    # Проверим, что появляется сообщение о неверном формате введенного телефона или email
    assert driver.find_element(By.XPATH,
                               "//span[contains(text(), 'Необходимо заполнить поле кириллицей. "
                               "От 2 до 30 символов.')]").is_displayed()


def test_reg_format_last_name():
    """Проверим, что система проверяет формат введенной фамилии"""
    driver.get(base_url)
    wait.until(EC.element_to_be_clickable((By.ID, 'kc-register')))
    driver.find_element(By.ID, 'kc-register').click()
    driver.find_element(By.NAME, 'lastName').send_keys(user_last_name_invalid_list[3] + Keys.TAB)

    # Проверим, что появляется сообщение о неверном формате введенного телефона или email
    assert driver.find_element(By.XPATH,
                               "//span[contains(text(), 'Необходимо заполнить поле кириллицей. "
                               "От 2 до 30 символов.')]").is_displayed()


def test_reg_format_email():
    """Проверим, что система проверяет формат введенного email"""
    driver.get(base_url)
    wait.until(EC.element_to_be_clickable((By.ID, 'kc-register')))
    driver.find_element(By.ID, 'kc-register').click()
    driver.find_element(By.ID, 'address').send_keys(email_invalid_list[0] + Keys.TAB)
    time.sleep(60)
    # Проверим, что появляется сообщение о неверном формате введенного телефона или email
    assert driver.find_element(By.XPATH, "//span[contains(text(), 'email в формате example@email.ru')]").is_displayed()


def test_reg_format_phone_or_email():
    """Проверим, что система проверяет формат введенного телефона"""
    driver.get(base_url)
    wait.until(EC.element_to_be_clickable((By.ID, 'kc-register')))
    driver.find_element(By.ID, 'kc-register').click()
    driver.find_element(By.ID, 'address').send_keys(phone_number_invalid_list[3] + Keys.TAB)

    # Проверим, что появляется сообщение о неверном формате введенного телефона или email
    assert driver.find_element(By.XPATH, "//span[contains(text(), 'Введите телефон в формате')]").is_displayed()


def test_reg_password_do_not_match():
    """Проверим, что система выдает сообщение если пароли не совпадают"""
    # В этом тесте работает Faker
    driver.get(base_url)
    wait.until(EC.element_to_be_clickable((By.ID, 'kc-register')))
    driver.find_element(By.ID, 'kc-register').click()
    driver.find_element(By.NAME, 'firstName').send_keys(fake_ru.first_name_female())
    driver.find_element(By.NAME, 'lastName').send_keys(fake_ru.last_name_female())
    driver.find_element(By.ID, 'address').send_keys(fake.unique.ascii_free_email())
    driver.find_element(By.ID, 'password'). \
        send_keys(fake.password(length=16, special_chars=True, digits=True, upper_case=True, lower_case=True))
    driver.find_element(By.ID, 'password-confirm'). \
        send_keys(fake.password(length=16, special_chars=True, digits=True, upper_case=True, lower_case=True))
    driver.find_element(By.NAME, 'register').click()

    # Проверим, что появляется сообщение "Пароли не совпадают"
    assert driver.find_element(By.XPATH, "//span[contains(text(), 'Пароли не совпадают')]").is_displayed()


def test_reg_format_password_symbol():
    """Проверим, что система проверяет формат пароля на наличие 1 спецсимвола или хотя бы одной цифры"""
    driver.get(base_url)
    wait.until(EC.element_to_be_clickable((By.ID, 'kc-register')))
    driver.find_element(By.ID, 'kc-register').click()
    driver.find_element(By.ID, 'password').send_keys(password_invalid_list[1] + Keys.TAB)

    # Проверим, что появляется сообщение о неверном формате введенного пароля
    assert driver.find_element(By.XPATH,
                               "//span[contains(text(), 'Пароль должен содержать хотя бы 1 спецсимвол или "
                               "хотя бы одну цифру')]").is_displayed()


def test_reg_format_password_capital():
    """Проверим, что система проверяет формат пароля на наличие хотя бы одной заглавной букву"""
    driver.get(base_url)
    wait.until(EC.element_to_be_clickable((By.ID, 'kc-register')))
    driver.find_element(By.ID, 'kc-register').click()
    driver.find_element(By.ID, 'password').send_keys(password_invalid_list[0] + Keys.TAB)

    # Проверим, что появляется сообщение о неверном формате введенного пароля
    assert driver.find_element(By.XPATH,
                               "//span[contains(text(), 'Пароль должен "
                               "содержать хотя бы одну заглавную букву')]").is_displayed()


def test_reg_format_password_len_min():
    """Проверим, что система проверяет минимальную длину пароля"""
    driver.get(base_url)
    wait.until(EC.element_to_be_clickable((By.ID, 'kc-register')))
    driver.find_element(By.ID, 'kc-register').click()
    driver.find_element(By.ID, 'password').send_keys(password_invalid_list[2] + Keys.TAB)

    # Проверим, что появляется сообщение о неверном формате введенного пароля
    assert driver.find_element(By.XPATH,
                               "//span[contains(text(), 'Длина пароля должна быть "
                               "не менее 8 символов')]").is_displayed()


def test_reg_format_password_len_max():
    """Проверим, что система проверяет длину пароля"""
    driver.get(base_url)
    wait.until(EC.element_to_be_clickable((By.ID, 'kc-register')))
    driver.find_element(By.ID, 'kc-register').click()
    driver.find_element(By.ID, 'password').send_keys(password_invalid_list[5] + Keys.TAB)

    # Проверим, что появляется сообщение о неверном формате введенного пароля
    assert driver.find_element(By.XPATH,
                               "//span[contains(text(), 'Длина пароля должна быть"
                               " не более 20 символов')]").is_displayed()


def test_reg_format_password_rus():
    """Проверим, что система не принимает пароль кириллицей"""
    driver.get(base_url)
    wait.until(EC.element_to_be_clickable((By.ID, 'kc-register')))
    driver.find_element(By.ID, 'kc-register').click()
    driver.find_element(By.ID, 'password').send_keys(password_invalid_list[6] + Keys.TAB)
    time.sleep(10)

    # Проверим, что появляется сообщение о неверном формате введенного пароля
    assert driver.find_element(By.XPATH,
                               "//span[contains(text(), 'Пароль должен содержать только "
                               "латинские буквы')]").is_displayed()


'''Регистрация нового пользователя по email'''


def test_reg_user_email():
    """Проверим, что пользователь зарегистрированный в системе не может повторно зарегистрироваться"""
    driver.get(base_url)
    wait.until(EC.element_to_be_clickable((By.ID, 'kc-register')))
    driver.find_element(By.ID, 'kc-register').click()
    driver.find_element(By.NAME, 'firstName').send_keys(user['name'])
    driver.find_element(By.NAME, 'lastName').send_keys(user['last_name'])
    """Здесь нужно ввести регион, но как?"""
    driver.find_element(By.ID, 'address').send_keys(email_valid)
    driver.find_element(By.ID, 'password').send_keys(password_valid)
    driver.find_element(By.ID, 'password-confirm').send_keys(password_valid)
    driver.find_element(By.NAME, 'register').click()

    # Проверим что появилось всплывающее окно учетная запись существует с кнопками войти и восстановить
    assert driver.find_element(By.NAME, 'gotoLogin').is_displayed()
    assert driver.find_element(By.ID, 'reg-err-reset-pass').is_displayed()


@pytest.mark.xfail
def test_reg_nev_user_email():
    """Регистрация нового пользователя по email"""
    """Для реализации этого теста необходимо иметь доступ к базе для получения проверочного кода, который
    отправлен на электронную почту пользователя"""
    driver.get(base_url)
    wait.until(EC.element_to_be_clickable((By.ID, 'kc-register')))
    driver.find_element(By.ID, 'kc-register').click()
    driver.find_element(By.NAME, 'firstName').send_keys(user['name'])
    driver.find_element(By.NAME, 'lastName').send_keys(user['last_name'])
    """Здесь нужно ввести регион, но как?"""
    driver.find_element(By.ID, 'address').send_keys(email_valid)
    driver.find_element(By.ID, 'password').send_keys(password_valid)
    driver.find_element(By.ID, 'password-confirm').send_keys(password_valid)
    driver.find_element(By.NAME, 'register').click()

    # Сообщение код подтверждения отправлен на email
    assert driver.find_element(By.CLASS_NAME, 'card-container__title').is_displayed()
    """В зависимости от формата полученного кода необходимо реализовать подтверждение полученного кода"""
    driver.find_element(By.ID, 'rt-code-0').send_keys(1)
    driver.find_element(By.ID, 'rt-code-1').send_keys(2)
    driver.find_element(By.ID, 'rt-code-2').send_keys(3)
    driver.find_element(By.ID, 'rt-code-3').send_keys(4)
    driver.find_element(By.ID, 'rt-code-4').send_keys(5)
    driver.find_element(By.ID, 'rt-code-5').send_keys(6)

    # Проверяем личные данные пользователя в личном кабинете
    assert driver.find_element(By.TAG_NAME, 'h2').text == f'{user["last_name"]}\n{user["name"]} {user["patronymic"]}'


'''Регистрация нового пользователя по номеру телефона'''


@pytest.mark.xfail
def test_reg_nev_user_phone():
    """Регистрация нового пользователя по телефону"""
    """Для реализации этого теста необходимо иметь доступ к базе для получения проверочного кода, который
    отправлен на номер телефона пользователя"""
    driver.get(base_url)
    wait.until(EC.element_to_be_clickable((By.ID, 'kc-register')))
    driver.find_element(By.ID, 'kc-register').click()
    driver.find_element(By.NAME, 'firstName').send_keys(user['name'])
    driver.find_element(By.NAME, 'lastName').send_keys(user['last_name'])
    """Здесь нужно ввести регион, но как?"""
    driver.find_element(By.ID, 'address').send_keys(phone_number_valid)
    driver.find_element(By.ID, 'password').send_keys(password_valid)
    driver.find_element(By.ID, 'password-confirm').send_keys(password_valid)
    driver.find_element(By.NAME, 'register').click()

    # Сообщение код подтверждения отправлен на email
    assert driver.find_element(By.CLASS_NAME, 'card-container__title').is_displayed()
    """В зависимости от формата полученного кода необходимо реализовать подтверждение полученного кода"""
    driver.find_element(By.ID, 'rt-code-0').send_keys(1)
    driver.find_element(By.ID, 'rt-code-1').send_keys(2)
    driver.find_element(By.ID, 'rt-code-2').send_keys(3)
    driver.find_element(By.ID, 'rt-code-3').send_keys(4)
    driver.find_element(By.ID, 'rt-code-4').send_keys(5)
    driver.find_element(By.ID, 'rt-code-5').send_keys(6)

    # Проверяем личные данные пользователя в личном кабинете
    assert driver.find_element(By.TAG_NAME, 'h2').text == f'{user["last_name"]}\n{user["name"]} {user["patronymic"]}'


'''Восстановление пароля'''


def test_password_recovery_invalid_captcha():
    """Проверим, что если не ввести Captcha появится сообщение о неверном тексте с картинки"""
    driver.get(recovery_url)
    wait.until(EC.element_to_be_clickable((By.ID, 'reset')))
    driver.find_element(By.ID, 't-btn-tab-mail').click()
    driver.find_element(By.ID, 'username').send_keys(email_valid)
    # здесь необходимо ввести Captcha
    driver.find_element(By.ID, 'reset').click()

    # Проверяем, что появляется сообщение: "Неверный логин или текст с картинки"
    assert driver.find_element(By.XPATH,
                               "//span[contains(text(), 'Неверный логин или текст с картинки')]").is_displayed()


def test_password_recovery():
    """Восстановление пароля по SMS на номер телефона"""
    driver.get(recovery_url)
    wait.until(EC.element_to_be_clickable((By.ID, 'reset')))
    driver.find_element(By.ID, 't-btn-tab-mail').click()
    driver.find_element(By.ID, 'username').send_keys(email_valid)
    # здесь необходимо ввести Captcha
    driver.find_element(By.ID, 'reset').click()

    # Проверяем, что появляется сообщение: "Неверный логин или текст с картинки"
    assert driver.find_element(By.XPATH,
                               "//span[contains(text(), 'Неверный логин или текст с картинки')]").is_displayed()


"""Авторизация по временному коду:"""




""" Проект теста для проверки регистрации со сложной параметризацией лучше не запускать"""


def generate_string(n):
    return 'x' * n


def russian_chars():
    return 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'


def chinese_chars():
    return '的一是不了人我在有他这为之大来以个中上们'


def special_chars():
    return '|\\/!@#$%^&*()-_=+`~?"№;:[]{}'


@pytest.mark.parametrize("phone",
                         [generate_string(9), generate_string(12), russian_chars(), russian_chars().upper(),
                          chinese_chars(), special_chars(), '123'],
                         ids=['9 symbols', '12 symbols', 'russian', 'RUSSIAN', 'chinese', 'specials', 'digit'])
@pytest.mark.parametrize("password",
                         [generate_string(1), generate_string(31), russian_chars(), russian_chars().upper(),
                          chinese_chars(), special_chars(), '123'],
                         ids=['9 symbols', '12 symbols', 'russian', 'RUSSIAN', 'chinese', 'specials', 'digit'])
@pytest.mark.parametrize("email",
                         [generate_string(1), generate_string(31), russian_chars(), russian_chars().upper(),
                          chinese_chars(), special_chars(), '123'],
                         ids=['1 symbols', '31 symbols', 'russian', 'RUSSIAN', 'chinese', 'specials', 'digit'])
@pytest.mark.parametrize("name",
                         [generate_string(1), generate_string(31), russian_chars(), russian_chars().upper(),
                          chinese_chars(), special_chars(), '123'],
                         ids=['1 symbols', '31 symbols', 'russian', 'RUSSIAN', 'chinese', 'specials', 'digit'])
@pytest.mark.parametrize("last_name",
                         [generate_string(1), generate_string(31), russian_chars(), russian_chars().upper(),
                          chinese_chars(), special_chars(), '123'],
                         ids=['1 symbols', '31', 'russian', 'RUSSIAN', 'chinese', 'specials', 'digit'])
def test_reg_nev_user_param(password, email, name, last_name):
    """Регистрация нового пользователя по email"""
    driver.get(base_url)
    wait.until(EC.element_to_be_clickable((By.ID, 'kc-register')))
    driver.find_element(By.ID, 'kc-register').click()
    driver.find_element(By.NAME, 'firstName').send_keys(name)
    driver.find_element(By.NAME, 'lastName').send_keys(last_name)
    driver.find_element(By.ID, 'address').send_keys(email)
    driver.find_element(By.ID, 'password').send_keys(password)
    driver.find_element(By.ID, 'password-confirm').send_keys(password)
    driver.find_element(By.NAME, 'register').click()
    time.sleep(3)
    # Сообщение: код подтверждения отправлен на email
    assert driver.find_element(By.CLASS_NAME, 'card-container__title').is_displayed()
    """В зависимости от формата полученного кода необходимо реализовать подтверждение полученного кода"""
    driver.find_element(By.ID, 'rt-code-0').send_keys(1)
    driver.find_element(By.ID, 'rt-code-1').send_keys(2)
    driver.find_element(By.ID, 'rt-code-2').send_keys(3)
    driver.find_element(By.ID, 'rt-code-3').send_keys(4)
    driver.find_element(By.ID, 'rt-code-4').send_keys(5)
    driver.find_element(By.ID, 'rt-code-5').send_keys(6)

    # Проверяем личные данные пользователя в личном кабинете
    assert driver.find_element(By.TAG_NAME,
                               'h2').text == f'{user["last_name"]}\n{user["name"]} {user["patronymic"]}'
