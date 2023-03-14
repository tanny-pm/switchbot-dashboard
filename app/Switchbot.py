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


class Switchbot:
    def __init__(self, access_token: str, secret: str):
        self.access_token = access_token
        self.secret = secret

    def __generate_sign(self, nonce: str = "") -> tuple[str, str]:
        """SWITCH BOT APIの認証キーを生成する"""

        t = int(round(time.time() * 1000))
        string_to_sign = "{}{}{}".format(self.access_token, t, nonce)
        string_to_sign_b = bytes(string_to_sign, "utf-8")
        secret_b = bytes(self.secret, "utf-8")
        sign = base64.b64encode(
            hmac.new(secret_b, msg=string_to_sign_b, digestmod=hashlib.sha256).digest()
        )

        return (str(t), str(sign, "utf-8"))

    def get_device_list(self) -> dict:
        """SWITCH BOTのデバイスリストを取得する"""

        nonce = "zzz"
        t, sign = self.__generate_sign(nonce)
        headers = {
            "Authorization": ACCESS_TOKEN,
            "t": t,
            "sign": sign,
            "nonce": nonce,
        }
        url = f"{API_BASE_URL}/v1.1/devices"
        try:
            r = requests.get(url, headers=headers)
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise ValueError(f"Switchbot request error: {e}")
        else:
            return r.json()["body"]["deviceList"]

    def get_device_status(self, device: dict) -> dict:
        """Switchbotデバイスのステータスを取得する"""

        nonce = "zzz"
        t, sign = self.__generate_sign(nonce)
        headers = {
            "Authorization": ACCESS_TOKEN,
            "t": t,
            "sign": sign,
            "nonce": nonce,
        }
        device_id = device["deviceId"]
        url = f"{API_BASE_URL}/v1.1/devices/{device_id}/status"

        try:
            r = requests.get(url, headers=headers)
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise ValueError(f"Switchbot request error: {e}")
        else:
            return r.json()["body"]


if __name__ == "__main__":
    # デバイスリストを出力する
    bot = Switchbot(ACCESS_TOKEN, SECRET)
    device_list = bot.get_device_list()

    with open("./device_list.json", "w") as f:
        f.write(json.dumps(device_list, indent=2, ensure_ascii=False))
