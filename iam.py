from info import *
from kit_speach import *
import requests
import time
import json
from datetime import datetime
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="log_file.txt",
    filemode="w",
    encoding='utf-8',
)

MAX_USERS = 3
MAX_SYMBOLS_FOR_USER = 600
MAX_TOKENS_FOR_USER = 600
MAX_SOUNDS_FOR_SST_FOR_USER = 20
MAX_TOKENS = 60


def create_new_token():
    logging.info("Создан iam токен")
    url = "http://169.254.169.254/computeMetadata/v1/instance/service-accounts/default/token"
    headers = {
        "Metadata-Flavor": "Google"
    }
    try:
        response = requests.get(url=url, headers=headers)
        if response.status_code == 200:
            token_data = response.json()  # вытаскиваем из ответа iam_token
            # добавляем время истечения iam_token к текущему времени
            token_data['expires_at'] = time.time() + token_data['expires_in']
            # записываем iam_token в файл
            with open("IAM_TOKEN", "w") as token_file:
                json.dump(token_data, token_file)
            return token_data["access_token"]  # возвращаем iam_token
    except Exception as e:
        print(f"Ошибка получения iam_token: {e}")


def get_creds():
    iam_token = "t1.9euelZqKipKemMuOmIyPyprGmo-Zxu3rnpWalseZi8qZjJKZyZSJlJKTx8nl8_cAdA1O-e8aDARM_N3z90AiC0757xoMBEz8zef1656Vmo6Jis7Llo3HlpHLjMyPz5bG7_zF656Vmo6Jis7Llo3HlpHLjMyPz5bGveuelZrKjJ6Qi8rGmJjJmpXIk56blbXehpzRnJCSj4qLmtGLmdKckJKPioua0pKai56bnoue0oye.OCtkozoYAjrOBxfkTuCD1VRk6sYsloJcDCEzuT4N6bJPeQ6ycBXoTMyz7-m8NKI0cFlP5K0WXsoXuDTdCa63AQ" # инициализируем переменную
    try:
        # чтение iam_token
        with open("IAM_TOKEN", 'r') as f:
            token_str = f.read().strip()
            # Предположим, что token_str имеет формат "access_token:expires_at"
            iam_token, expires_at = token_str.split(":")
            expiration = datetime.strptime(expires_at, "%Y-%m-%dT%H:%M:%S.%f")
        # если срок годности истёк
        if expiration < datetime.now():
            logging.info("Срок годности iam_token истёк")
            # получаем новый iam_token
            iam_token = create_new_token()
    except:
        # если что-то пошло не так - получаем новый iam_token
        iam_token = create_new_token()
        if iam_token == None:
            iam_token = "t1.9euelZqKipKemMuOmIyPyprGmo-Zxu3rnpWalseZi8qZjJKZyZSJlJKTx8nl8_cAdA1O-e8aDARM_N3z90AiC0757xoMBEz8zef1656Vmo6Jis7Llo3HlpHLjMyPz5bG7_zF656Vmo6Jis7Llo3HlpHLjMyPz5bGveuelZrKjJ6Qi8rGmJjJmpXIk56blbXehpzRnJCSj4qLmtGLmdKckJKPioua0pKai56bnoue0oye.OCtkozoYAjrOBxfkTuCD1VRk6sYsloJcDCEzuT4N6bJPeQ6ycBXoTMyz7-m8NKI0cFlP5K0WXsoXuDTdCa63AQ"

    print(iam_token)
    return iam_token
