import os
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from config import api_id, api_hash, device_token, sdk, app_ver, proxy_gate

session_file_path = '/home/live/Downloads/+79326315411'


def session_string():
    client = TelegramClient(session_file_path,
                            api_id, api_hash,
                            device_model=device_token,
                            system_version=sdk,
                            app_version=app_ver,
                            proxy=proxy_gate,)

    with client:
        session = client.session
        string_session = StringSession.save(session)
        # me = client.get_me()
        # print(me.phone)
        # print("Номер телефона:", me)
        print("Ваша строка сессии:", string_session)


def tdata_sesion():

    # Путь к папке tdata
    tdata_folder = '/home/live/Downloads/+79291207937/tdata'

    # Список файлов в папке
    files = os.listdir(tdata_folder)

    # Перебираем файлы в папке и конвертируем их в .session
    for file_name in files:
        if file_name.endswith('.json'):
            file_path = os.path.join(tdata_folder, file_name)
            with open(file_path, 'r') as file:
                session_data = file.read()
                string_session = StringSession(session_data)
                session_file_name = os.path.splitext(file_name)[0] + '.session'
                session_file_path = os.path.join(tdata_folder, session_file_name)
                with open(session_file_path, 'w') as session_file:
                    session_file.write(string_session.save())
                    print(f"Конвертирован файл: {file_name} в {session_file_name}")


session_string()
