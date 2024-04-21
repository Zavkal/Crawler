import asyncio
from random import random

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from app import config

random_time_seed = random()


# Проверка на бан тг
async def check_tg(phones: list, driver):
    driver.get('https://web.telegram.org/?legacy=1#/im')
    list_perebora_phones = phones.copy()
    await asyncio.sleep(random_time_seed + 2.5)
    for phone in list_perebora_phones:
        phone_input = WebDriverWait(driver, 90).until(ec.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[3]/div[2]/form/div[2]/div[2]/input")))
        phone_input.clear()
        if config.path_time:
            await asyncio.sleep(random_time_seed)
        phone_input.send_keys(phone[2:])
        if phone == list_perebora_phones[0]:
            await asyncio.sleep(2)
        await asyncio.sleep(random_time_seed + 0.2)
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
                await asyncio.sleep(random_time_seed)
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
                await asyncio.sleep(random_time_seed)
                driver.quit()
                options = webdriver.ChromeOptions()
                driver = webdriver.Chrome(options=options)
                await check_tg(phones, driver)
            except:
                pass
    driver.quit()
    return



