import asyncio
from scanner import scan_loop


if __name__ == "__main__":

    print("Starting BLE Attendance Scanner...")

    asyncio.run(scan_loop())