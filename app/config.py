# Обязательно пишем путь до браузера. Вносим только путь до файла в кавычки r"путь"
import json

path_chrome = r""  # В случае, когда не работает, оставьте путь пустым. Выглядеть будет r""

# Поставить значение 1, если всплывающих окон больше нет.
captcha_cookie = 5  # Мы используем куки
captcha_eva = 5  # История с Евой

# Когда номер указывается в коде страны, выставляем True. Если ошибок нет, оставляем False.
path_time = False
# Открываем json с настройками
with open('/home/live/Downloads/+79326315411.json', 'r') as file:
    session_data = json.load(file)

api_id = session_data['app_id']
api_hash = session_data['app_hash']
device_token = session_data['device']
app_ver = session_data['app_version']
sdk = session_data['sdk']


# Прокси
proxies = "2c264def66:69cf64226e:178.234.28.84:41791"
proxy_parts = proxies.split(":")
proxy_ip = proxy_parts[-2]
proxy_port = int(proxy_parts[-1])
proxy_user = proxy_parts[0]
proxy_password = proxy_parts[1]
proxy_gate = {"proxy_type": "socks5", "addr": proxy_ip, "port": proxy_port,
              "username": proxy_user, "password": proxy_password, }

