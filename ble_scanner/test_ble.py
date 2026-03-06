import asyncio
from bleak import BleakScanner


async def test():

    print("Scanning for BLE devices...\n")

    devices = await BleakScanner.discover(timeout=5, return_adv=True)

    for address, (device, adv) in devices.items():

        print(
            "Name:", device.name,
            "Address:", device.address,
            "RSSI:", adv.rssi
        )


asyncio.run(test())