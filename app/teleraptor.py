import asyncio
import concurrent.futures
import time

from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.functions.contacts import ImportContactsRequest
from telethon.tl.types import InputPhoneContact
from app.config import proxy_gate, api_id, api_hash, app_ver, device_token, sdk


async def check_telegram_account(session_string, phone, tt=10):
    print(f"Проверка номера {phone}")
    client = TelegramClient(StringSession(session_string),
                            api_id, api_hash,
                            proxy=proxy_gate,
                            app_version=app_ver,
                            device_model=device_token,
                            system_version=sdk,
                            connection_retries=20)
    try:
        await client.start()
        # Добавляем в контакты
        a = await client(ImportContactsRequest(
            [InputPhoneContact(client_id=0, phone=phone, first_name=f"{phone}", last_name=" ")]))
        imp = a.imported[0].user_id
        print(f"Номер {phone} существует.")

    except Exception as e:
        # Если не удалось добавить номер в контакты, отправляем сообщение в чат
        print(f"Номер {phone} не существует.")
        with open(r'valid1.txt', 'a') as file:
            file.write(phone + '\n')
    finally:
        await client.disconnect()
    await asyncio.sleep(tt)


async def main():
    valid_phones = []
    with open(r'valid.txt', 'r') as file:
        phones = file.readlines()
        for i in phones:
            if len(i) > 12:
                valid_phones.append(i[:-1])
            else:
                valid_phones.append(i)

    # Чтение строки сессии из файла
    with open(r"app/session_file.txt", 'r') as f:
        session_string = f.read().strip()

    # Создание пула потоков
    loop = asyncio.get_running_loop()
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        # Запуск каждой задачи
        tasks = []
        for phone in valid_phones:
            task = await loop.run_in_executor(executor, check_telegram_account, session_string, phone)
            tasks.append(task)

        # Ожидание завершения всех задач
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
