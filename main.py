import asyncio
import time

from selenium import webdriver
from app.telegram_ban import check_tg, check_tg2
from app.megafon import login_lk
import logging
from app import config
from app.teleraptor import main as teleraptor_main

# Настройка конфигурации логгера
logging.basicConfig(filename='app/errors.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')


# Создаем экземпляр опций Chromium
chrome_options = webdriver.ChromeOptions()

# Указываем путь к исполняемому файлу ChromeDriver
if len(config.path_chrome) > 0:
    chrome_options.binary_location = config.path_chrome


def parsing_megafon(number_password):
    number_password = number_password.split(":")
    number = number_password[0]
    password = number_password[1]
    # chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    if len(number) > 10:
        number = number[-10:]
    login_lk(driver=driver, phone=number, password=password)
# Закрываем драйвер с текущими опциями
    return


def check_ban(number):
    a = time.time()
    with open("valid.txt", "w"):
        pass
    options = webdriver.ChromeOptions()

    driver = webdriver.Chrome(options=options)
    check_tg(phones=number, driver=driver)
    b = time.time()
    print(f" Время выполнения проверки {int(b - a)} сек.")
    return


while True:
    print()
    print('Разработка Back-end сайта, приложений, скриптов - тг @peoplemyfriends\n',
        '1 - Получение номеров с Мегафона\n',
        '2 - Проверка на бан тг из файла all_phones.txt\n',
        '3 - Получение номеров и проверка на бан.\n',
        '4 - Проверка на наличие аккаунта.\n',
        '5 - Проверка на бан с получением номеров из консоли.\n',
        '6 - Поиск воркера')
    print()

    counter = int(input())

    try:
        if counter == 1:
            megafon = input("Введите номер телефона и пароль в формате НОМЕР:ПАРОЛЬ \n")
            parsing_megafon(number_password=megafon)

        if counter == 2:
            test = []
            with open("app/all_phones.txt", "r") as f:
                numbers = f.readlines()
                for i in numbers:
                    test.append(i.strip())
                numbers = test[:]
                for i in range(numbers.count("")):
                    numbers.remove("")
            print(f"На проверке {len(numbers)} номеров")
            check_ban(number=numbers)

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
                for i in range(numbers.count("")):
                    numbers.remove("")
            time.sleep(1)
            print(f"На проверке {len(numbers)} номеров")
            check_ban(number=numbers)

        if counter == 4:
            with open("valid1.txt", "w"):
                pass

            async def run_teleraptor():
                await teleraptor_main()

            asyncio.run(run_teleraptor())

        if counter == 5:
            test = list(input().strip().split())
            print(f"На проверке {len(test)} номеров")
            check_ban(number=test)

        if counter == 6:
            test = []
            with open("valid.txt", "r") as f:
                numbers = f.readlines()
                for i in numbers:
                    test.append(i.strip())
            options = webdriver.ChromeOptions()
            options.add_argument("user-data-dir=/home/live/snap/chromium/common/chromium")
            options.add_argument("--profile-directory=Default")
            driver = webdriver.Chrome(options=options)
            check_tg2(valid_phones=test, driver=driver)
            driver.quit()
            driver.close()

    except Exception as e:
        # Логирование ошибки
        logging.error("An error occurred: %s", str(e), exc_info=True)
