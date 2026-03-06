import requests
from config import API_URL
from offline_store import save_offline


def send_devices(payload):

    try:

        r = requests.post(API_URL, json=payload, timeout=5)

        print("Sent to backend:", r.status_code)

    except Exception as e:

        print("Backend offline. Saving locally.")

        save_offline(payload)