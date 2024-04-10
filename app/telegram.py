import asyncio
import time
from random import random

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

random_time_seed = random()


with open(r'valid_phones_crawler.txt', 'w'):
    pass

phones = []
with open(r'valid.txt', 'r') as file:
    lines = file.readlines()
    for el in lines:
        el = el.replace(' ', '')
        el = el.replace('\n', '')
        phones.append(el)


async def check_tg2(valid_phones, driver):
    try:
        list_phones = valid_phones.copy()
        # --------------------------------------------------------------------
        driver.get("https://web.telegram.org/a/")
        time.sleep(3)
        #  Находим кнопку открывания меню
        WebDriverWait(driver, 90).until(ec.presence_of_element_located(
                                                            (By.CLASS_NAME, "ripple-container"))).click()
        time.sleep(2)
        driver.find_element(By.XPATH, '//*[text()="Contacts"]').click()
        time.sleep(1)
        print("Подключился к Телеграм")
        for phone in list_phones:
            #  Кликаем кнопку добавления контакта
            driver.find_element("css selector", 'button[title="Create New Contact"]').click()
            time.sleep(1)
            #  Кликаем кнопку, где вводится телефон
            phone_input = driver.find_element(By.XPATH, '//input[@aria-label="Phone Number"]')
            phone_input.click()
            phone_input.clear()
            time.sleep(1)
            phone_input.send_keys(phone)
            #  Кликаем кнопку ввода имени
            name_input = driver.find_element(By.XPATH, '//input[@aria-label="First name (required)"]')
            name_input.click()
            name_input.clear()
            time.sleep(1)
            name_input.send_keys(phone)
            time.sleep(1)
            #  Кликаем кнопку "Продолжить"
            driver.find_element(By.XPATH, '//button[text()="Done"]').click()

            #  Проверка на вывод сообщения: Такого контакта нет в телеграм
            try:
                WebDriverWait(driver, 4).until(ec.presence_of_element_located(
                    (By.CLASS_NAME, 'Notification-container')))
                driver.find_element(By.XPATH, '//button[text()="Cancel"]').click()
                print("Элемент найден, аккаунт не зарегистрирован.")
                with open(r'valid_phones_crawler.txt', 'a') as file1:
                    file1.write(phone + '\n')
                valid_phones.remove(phone)

            except TimeoutException:
                print("Элемент не найден. Аккаунт есть в телеграм")
                time.sleep(1.3)
            time.sleep(2)
    except:
        await check_tg2(valid_phones, driver)

    with open(r'all_phones.txt', 'w'):
        pass

    with open(r'valid.txt', 'w'):
        pass


