import asyncio
import time
from random import random

from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from app import config

random_time_seed = random()


# Проверка на бан тг
def check_tg(phones: list, driver):
    driver.get('https://web.telegram.org/?legacy=1#/im')
    list_perebora_phones = phones.copy()
    time.sleep(random_time_seed + 2.5)
    for phone in list_perebora_phones:
        phone_input = WebDriverWait(driver, 90).until(ec.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[3]/div[2]/form/div[2]/div[2]/input")))
        phone_input.clear()
        if config.path_time:
            time.sleep(random_time_seed)
        phone_input.send_keys(phone[2:])
        if phone == list_perebora_phones[0]:
            time.sleep(2)
        time.sleep(random_time_seed + 0.2)
        next_btn = driver.find_element(By.CLASS_NAME, "login_head_submit_btn")
        next_btn.click()
        WebDriverWait(driver, 60).until(ec.presence_of_element_located((By.CLASS_NAME, "btn-md-primary"))).click()
        try:
            check_ban = WebDriverWait(driver, 4+random_time_seed).until(ec.presence_of_element_located((By.XPATH, "//*[text()='Error']")))
            print(f'Номер {phone} невалидный')
            phones.remove(phone)
            driver.find_element(By.CLASS_NAME, "btn-md-primary").click()
        except:
            try:
                time.sleep(random_time_seed)
                driver.find_element(By.NAME, "phone_code")
                print(f'Номер {phone} валидный')
                with open(r'valid.txt', 'a') as file:
                    file.write(phone + "\n")
                phones.remove(phone)
                driver.find_element(By.CLASS_NAME, "login_edit_phone").click()

            except:
                pass
            try:
                driver.find_element(By.XPATH, "//*[text()='Too fast']")
                print(f'Поймал Flood Wait на номере {phone}. Проверим его в последнюю очередь')
                phones.remove(phone)
                phones.append(phone)
                print(f"Осталось проверить {len(phones)} номеров")
                driver.delete_all_cookies()
                time.sleep(random_time_seed)
                driver.quit()
                options = webdriver.ChromeOptions()
                driver = webdriver.Chrome(options=options)
                check_tg(phones, driver)
            except:
                pass
    driver.quit()
    return


def check_tg2(valid_phones: list, driver):
    count = 0
    list_valid = []
    list_phones = valid_phones
    # --------------------------------------------------------------------
    driver.get("https://web.telegram.org/a/")
    time.sleep(3)
    #  Находим кнопку открывания меню
    WebDriverWait(driver, 15).until(ec.presence_of_element_located(
                                                        (By.CLASS_NAME, "ripple-container"))).click()
    time.sleep(2)
    driver.find_element(By.XPATH, '//*[text()="Contacts"]').click()
    for phone in list_phones:
        time.sleep(random_time_seed + 1)
        #  Кликаем кнопку добавления контакта
        driver.find_element("css selector", 'button[title="Create New Contact"]').click()
        time.sleep(random_time_seed + 1)
        #  Кликаем кнопку, где вводится телефон
        phone_input = driver.find_element(By.XPATH, '//input[@aria-label="Phone Number"]')
        phone_input.click()
        phone_input.clear()
        phone_input.send_keys(phone)
        time.sleep(random_time_seed)
        #  Кликаем кнопку ввода имени
        name_input = driver.find_element(By.XPATH, '//input[@aria-label="First name (required)"]')
        name_input.click()
        name_input.clear()
        name_input.send_keys(phone)
        time.sleep(random_time_seed)
        #  Кликаем кнопку "Продолжить"
        driver.find_element(By.XPATH, '//button[text()="Done"]').click()

        #  Проверка на вывод сообщения: Такого контакта нет в телеграм
        try:
            WebDriverWait(driver, 4).until(ec.presence_of_element_located(
                (By.CLASS_NAME, 'Notification-container')))
            driver.find_element(By.XPATH, '//button[text()="Cancel"]').click()
            list_valid.append(phone)
            print(f"Нет контакта {phone}")
        except TimeoutException:
            pass

    time.sleep(2)
    return list_valid
