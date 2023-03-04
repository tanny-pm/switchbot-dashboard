import base64
import hashlib
import hmac
import json
import os
import time

import requests
from dotenv import load_dotenv

load_dotenv(".env")

API_BASE_URL = "https://api.switch-bot.com"

ACCESS_TOKEN: str = os.environ["SWITCHBOT_ACCESS_TOKEN"]
SECRET: str = os.environ["SWITCHBOT_SECRET"]


def generate_sign(token: str, secret: str, nonce: str) -> tuple[str, str]:
    """SWITCH BOT APIの認証キーを生成する"""

    t = int(round(time.time() * 1000))
    string_to_sign = "{}{}{}".format(token, t, nonce)
    string_to_sign_b = bytes(string_to_sign, "utf-8")
    secret_b = bytes(secret, "utf-8")
    sign = base64.b64encode(
        hmac.new(secret_b, msg=string_to_sign_b, digestmod=hashlib.sha256).digest()
    )

    return (str(t), str(sign, "utf-8"))


def get_device_list() -> str:
    """SWITCH BOTのデバイスリストを取得する"""

    nonce = "zzz"
    t, sign = generate_sign(ACCESS_TOKEN, SECRET, nonce)
    headers = {
        "Authorization": ACCESS_TOKEN,
        "t": t,
        "sign": sign,
        "nonce": nonce,
    }
    url = f"{API_BASE_URL}/v1.1/devices"
    r = requests.get(url, headers=headers)

    return json.dumps(r.json(), indent=2, ensure_ascii=False)


if __name__ == "__main__":
    r = get_device_list()
    print(r)

    with open("./device_list.json", "w") as f:
        f.write(r)
