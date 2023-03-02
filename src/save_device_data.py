import base64
import hashlib
import hmac
import json
import os
import time

import requests
from dotenv import load_dotenv
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

load_dotenv(".env")

# InfluxDB
INFLUXDB_TOKEN = os.environ["INFLUXDB_TOKEN"]
bucket = "switchbot"
client = InfluxDBClient(url="http://localhost:8086", token=INFLUXDB_TOKEN, org="org")
write_api = client.write_api(write_options=SYNCHRONOUS)
query_api = client.query_api()

# SwitchBot
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


def get_device_status(device: dict) -> dict:
    """Switchbotデバイスのステータスを取得する"""

    nonce = "zzz"
    t, sign = generate_sign(ACCESS_TOKEN, SECRET, nonce)
    headers = {
        "Authorization": ACCESS_TOKEN,
        "t": t,
        "sign": sign,
        "nonce": nonce,
    }
    device_id = device["deviceId"]
    url = f"{API_BASE_URL}/v1.1/devices/{device_id}/status"

    r = requests.get(url, headers=headers)

    device_data = r.json()["body"]

    return device_data


def save_device_status(status: dict):
    """SwitchbotデバイスのステータスをInfluxDBに保存する"""

    device_type = status.get("deviceType")

    if device_type == "MeterPlus":
        p = (
            Point("MeterPlus")
            .tag("device_id", status["deviceId"])
            .field("humidity", status["humidity"])
            .field("temperature", status["temperature"])
        )
        write_api.write(bucket=bucket, record=p)
        print(f"Save:{status}")


if __name__ == "__main__":

    with open("device_list.json", "r") as f:
        s = json.load(f)
        device_list = s["body"]["deviceList"]

    for d in device_list:
        print(d)
        status = get_device_status(d)
        try:
            save_device_status(status)
        except Exception as e:
            print(f"Error: {e}")
