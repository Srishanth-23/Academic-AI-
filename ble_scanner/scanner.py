import asyncio
from bleak import BleakScanner

from config import SCAN_DURATION, SCAN_INTERVAL, RSSI_THRESHOLD, SCANNER_ID
from api_client import send_devices


async def scan_loop():

    while True:

        print("Scanning classroom...")

        devices = await BleakScanner.discover(timeout=SCAN_DURATION, return_adv=True)

        detected = []

        for address, (device, adv) in devices.items():

            rssi = adv.rssi

            if rssi > RSSI_THRESHOLD:

                detected.append({
                    "device_id": device.address,
                    "rssi": rssi
                })

        if detected:

            payload = {
                "scanner_id": SCANNER_ID,
                "devices": detected
            }

            print("Detected:", payload)

            send_devices(payload)

        else:

            print("No nearby devices")

        await asyncio.sleep(SCAN_INTERVAL)