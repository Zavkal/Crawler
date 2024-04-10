import asyncio
import time
from random import random

from selenium.common import TimeoutException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

random_time_seed = random()




# Проверка на бан тг
async def check_tg(phones, driver):
    driver.get('https://web.telegram.org/?legacy=1#/im')
    list_perebora_phones = phones.copy()
    for phone in list_perebora_phones:
        phone_input = WebDriverWait(driver, 90).until(ec.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[3]/div[2]/form/div[2]/div[2]/input")))
        await asyncio.sleep(1)
        phone_input.clear()
        phone_input.send_keys(phone[2:])
        await asyncio.sleep(random_time_seed + 2)
        next_btn = driver.find_element(By.CLASS_NAME, "login_head_submit_btn")
        next_btn.click()
        WebDriverWait(driver, 60).until(ec.presence_of_element_located((By.CLASS_NAME, "btn-md-primary"))).click()
        try:
            check_ban = WebDriverWait(driver, 5).until(ec.presence_of_element_located((By.XPATH, "//*[text()='Error']")))
            btn_ok = WebDriverWait(driver, 30).until(ec.presence_of_element_located((By.CLASS_NAME, "btn-md-primary")))
            print(f'Номер {phone} НЕвалидный!')
            phones.remove(phone)
            btn_ok.click()
        except:
            try:
                flood_wait = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.XPATH, "//*[text()='Too fast']")))
                print(f'Поймал Flood Wait на номере {phone}. Чекнем его в последнюю очередь')
                phones.remove(phone)
                phones.append(phone)
                driver.delete_all_cookies()
                await asyncio.sleep(random_time_seed + 2)
                driver.quit()
                options = webdriver.ChromeOptions()
                options.add_argument('--incognito')
                driver = webdriver.Chrome(options=options)
                await check_tg(phones, driver)
            except:
                pass
            try:
                approve_btn = WebDriverWait(driver, 45).until(ec.presence_of_element_located((By.NAME, "phone_code")))
                edit_btn = WebDriverWait(driver, 30).until(ec.presence_of_element_located((By.CLASS_NAME, "login_edit_phone")))
                print(f'Номер {phone} валидный!')
                with open(r'app/valid.txt', 'a') as file:
                    file.write(phone + "\n")
                phones.remove(phone)
                edit_btn.click()
            except:
                print(f'~~~ Ошибка на номере {phone}. Чекнем его в последнюю очередь ~~~')
                try:
                    phones.remove(phone)
                except:
                    return
                phones.append(phone)
                driver.delete_all_cookies()
                driver.quit()
                options = webdriver.ChromeOptions()
                options.add_argument('--incognito')
                driver = webdriver.Chrome(options=options)
                await check_tg(phones, driver)
    print('Проверка завершена')
    return



