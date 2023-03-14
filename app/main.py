import base64
import hashlib
import hmac
import json
import os
import time
from time import sleep

import requests
import schedule
from dotenv import load_dotenv
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from Switchbot import Switchbot

load_dotenv(".env")

# InfluxDB
INFLUXDB_TOKEN = os.environ["INFLUXDB_TOKEN"]
bucket = "switchbot"
client = InfluxDBClient(url="http://influxdb:8086", token=INFLUXDB_TOKEN, org="org")
write_api = client.write_api(write_options=SYNCHRONOUS)
query_api = client.query_api()

# SwitchBot
ACCESS_TOKEN: str = os.environ["SWITCHBOT_ACCESS_TOKEN"]
SECRET: str = os.environ["SWITCHBOT_SECRET"]


def save_device_status(status: dict):
    """SwitchbotデバイスのステータスをInfluxDBに保存する"""

    device_type = status.get("deviceType")

    if device_type == "MeterPlus":
        p = (
            Point("MeterPlus")
            .tag("device_id", status["deviceId"])
            .field("humidity", float(status["humidity"]))
            .field("temperature", float(status["temperature"]))
        )

        write_api.write(bucket=bucket, record=p)
        print(f"Saved:{status}")


def task():
    """定期実行するタスク"""
    bot = Switchbot(ACCESS_TOKEN, SECRET)

    with open("device_list.json", "r") as f:
        device_list = json.load(f)

    for d in device_list:
        device_type = d.get("deviceType")
        if device_type == "MeterPlus":
            try:
                status = bot.get_device_status(d)
            except Exception as e:
                print(f"Request error: {e}")
                continue

            try:
                save_device_status(status)
            except Exception as e:
                print(f"Save error: {e}")


if __name__ == "__main__":
    schedule.every(5).minutes.do(task)

    while True:
        schedule.run_pending()
        sleep(1)
