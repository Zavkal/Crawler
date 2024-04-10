import socks
from telethon.sync import TelegramClient
import random
import asyncio
from multiprocessing import Process, Queue


with open(r'proxy.txt', 'r') as proxy_file:
    proxy = proxy_file.readlines()

list_session = []
session_file_path = f'/home/live/Downloads/{list_session}.session'
api_hash = "b18441a1ff607e10a989891a5462e627"
api_id = 2040
# Создайте объект TelegramClient с указанием пути к файлу сессии


async def check_telegram_account(number, proxies, file_path, tt=21):
    list_phones = number.copy()
    for phone in list_phones:
        proxy_string = random.choice(proxies)
        proxy_parts = proxy_string.strip().split(':')
        proxy_ip = proxy_parts[-2]
        proxy_port = int(proxy_parts[-1])
        proxy_user = proxy_parts[0]
        proxy_password = proxy_parts[1]
        proxy_gate = {"proxy_type": socks.HTTP, "addr": proxy_ip, "port": proxy_port,
                      "username": proxy_user, "password": proxy_password}
        client = TelegramClient(file_path, api_id, api_hash, proxy=proxy_gate)
        async with client:
            try:
                # Получаем сущность (пользователя) по номеру телефона
                entity = await client.get_entity(phone)
                print(f"Аккаунт с номером {phone} существует.")
                print(entity)
            except ValueError:
                print(f"Аккаунт с номером {phone} не существует.")
                with open(r'valid1.txt', 'a') as file1:
                    file1.write(phone + '\n')

        await asyncio.sleep(tt)

# Удаляем содержимое файла
with open(r"valid1.txt", 'w'):
    pass

# Открываем список номеров и копируем его
valid_phones = []
with open(r'all_phones.txt', 'r') as phones_file:
    lines = phones_file.readlines()
    for el in lines:
        el = el.replace(' ', '')
        el = el.replace('\n', '')
        valid_phones.append(el)

# Читаем файл с прокси. (ОБЯЗАТЕЛЬНО В ФОРМАТЕ ЛОГИН, ПАРОЛЬ, ХОСТ, ПОРТ)
with open(r'proxy.txt', 'r') as proxy_file:
    proxy = proxy_file.readlines()

# Запускаем асинхронную функцию проверки аккаунта
asyncio.run(check_telegram_account(proxies=proxy, number=valid_phones, file_path=session_file_path))
