import asyncio
import time
from selenium import webdriver
# from telegram import check_tg2
from app.telegram_ban import check_tg
from app.megafon import login_lk
import logging

# Настройка конфигурации логгера
logging.basicConfig(filename='errors.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')


# Создаем экземпляр опций Chromium
chrome_options = webdriver.ChromeOptions()

# Указываем путь к исполняемому файлу ChromeDriver
# chrome_options.binary_location = '/usr/bin/chromium-browser'


def parsing_megafon(number_password):
    number_password = number_password.split(":")
    number = number_password[0]
    password = number_password[1]
    # chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    if len(number) > 10:
        number = number[-10:]
    parsing = login_lk(driver=driver, phone=number, password=password)
# Закрываем драйвер с текущими опциями
    driver.quit()
    return parsing


async def check_ban(number):
    with open("app/valid.txt", "w"):
        pass
    options = webdriver.ChromeOptions()
    options.add_argument('--incognito')
    driver = webdriver.Chrome(options=options)
    list_valid = await check_tg(phones=number, driver=driver)
    return




while True:
    print('Разработка Back-end сайта, приложений, скриптов - тг @peoplemyfriends\n',
         '1 - Получение номеров с Мегафона\n',
        '2 - Проверка на бан тг из файла all_phones.txt\n',
        '3 - Получение номеров и проверка на бан.')


    counter = int(input())



    try:
        if counter == 1:
            megafon = input("Введите номер телефона и пароль форматом: НОМЕР:ПАРОЛЬ \n")
            parsing_megafon(number_password=megafon)

        if counter == 2:
            test = []
            with open("app/all_phones.txt", "r") as f:
                numbers = f.readlines()
                for i in numbers:
                    test.append(i.strip())
                numbers = test[:]
            asyncio.run(check_ban(number=numbers))

        if counter == 3:
            megafon = input("Введите номер телефона и пароль форматом: НОМЕР:ПАРОЛЬ \n")
            parsing_megafon(number_password=megafon)
            print("Включение проверки...")
            test = []
            with open("app/all_phones.txt", "r") as f:
                numbers = f.readlines()
                for i in numbers:
                    test.append(i.strip())
                numbers = test[:]
            time.sleep(3)
            asyncio.run(check_ban(number=numbers))
    except Exception as e:
        # Логирование ошибки
        logging.error("An error occurred: %s", str(e), exc_info=True)








# async def numcrawler(number):
#     chrome_options.add_argument("user-data-dir=/home/live/snap/chromium/common/chromium")
#     chrome_options.add_argument("--profile-directory=Default")
#     # chrome_options.add_argument("--headless")
#     # Создаем экземпляр драйвера для Chromium с указанными опциями
#     driver = webdriver.Chrome(options=chrome_options)
#     list_valid = await check_tg2(driver=driver, valid_phones=number)
#     return list_valid

# async def teleraptor(number, proxies):
#     pass
# with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
