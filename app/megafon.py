import time
from random import random

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


def login_lk(phone, password, driver, ):
    with open("app/all_phones.txt", "w"):
        pass
    # Открываем браузер и переходим на указанный URL
    driver.get("https://lk.megafon.ru/")
    random_time_seed = random() + 1
    # Указываем задержку с рандомным зерном от возможности быстрой блокировки IP
    time.sleep(random_time_seed)
    try:
        # Находим элемент "Вход по паролю" и кликаем
        driver.find_element(By.XPATH, '//*[contains(text(), "Вход по паролю")]').click()

        # Если элемент найден, выводим сообщение об успешном прохождении теста
        print("Начало работы")
        phone_input = driver.find_element(By.CLASS_NAME, 'phone-input__field')
        phone_input.clear()
        phone_input.send_keys(phone)
        time.sleep(random_time_seed)
        password_input = driver.find_element(By.CLASS_NAME, 'text-field__input')
        password_input.clear()
        password_input.send_keys(password)
        time.sleep(random_time_seed)
        driver.find_element(By.CLASS_NAME, "mfui-checkbox__label").click()
        time.sleep(random_time_seed)
        driver.find_element(By.CLASS_NAME, "mfui-button__inner").click()
        time.sleep(random_time_seed + 1)

    except:
        # Если элемент не найден, выводим сообщение об ошибке
        print("Что-то пошло не так. Обратись к разработчику.")
        return

        # Проверка капчи и отсеивание
    try:
        driver.find_element(By.XPATH, "//*[text()='Введите код с картинки (Код ошибки: a211)']")
        print('Запрошена CAPTCHA. Введи самостоятельно')
        phone_input = driver.find_element(By.CLASS_NAME, 'phone-input__field')
        phone_input.clear()
        phone_input.send_keys(phone)
        password_input = driver.find_element(By.CLASS_NAME, 'text-field__input')
        password_input.clear()
        password_input.send_keys(password)
        driver.find_element(By.CLASS_NAME, "mfui-checkbox__label").click()
        time.sleep(random_time_seed)
        driver.find_element(By.CLASS_NAME, "mfui-button__inner").click()
        time.sleep(random_time_seed)
    except:
        pass

    # Парсинг
    WebDriverWait(driver, 120).until(ec.url_changes('https://lk.megafon.ru'))
    time.sleep(random_time_seed)
    #  Отсеиваем появления окна с историями
    try:
        WebDriverWait(driver, 15).until(
            ec.presence_of_element_located((By.CLASS_NAME, "popup")))
        driver.find_element(By.XPATH, "//button[@data-testid='CookiesAssent-submitButton']").click()
    except:
        pass
    WebDriverWait(driver, 30).until(
        ec.presence_of_element_located((By.XPATH, "//*[text()='Доп. номер']"))
                                            ).click()
    WebDriverWait(driver, 30).until(
        ec.presence_of_element_located((By.CLASS_NAME, "ym-service-shelf-additional-numbers-connection"))
                                            ).click()
    WebDriverWait(driver, 30).until(
        ec.presence_of_element_located((By.XPATH, "//*[text()='Продолжить']"))
                                            ).click()
    WebDriverWait(driver, 30).until(
        ec.presence_of_element_located((By.CLASS_NAME, "mfui-select__inner"))
                                            ).click()

    phones = driver.find_elements(By.CLASS_NAME, 'mfui-select__item-title')
    print("Собрали номера с ЛК")

    # Записываем список номеров в тестовый файл all_phones
    all_phones = []
    for el in phones:
        all_phones.append(el.text)
        print(el.text)
    with open(r'app/all_phones.txt', 'w') as file:
        for el in all_phones:
            el = el.replace('-', '')
            el = el.replace(' ', '')
            file.write(el + '\n')
        time.sleep(2)
