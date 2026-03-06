from sqlalchemy.orm import Session
from app.models.ble_log import BLELog


def save_ble_devices(db: Session, devices, scanner_id):

    saved = []

    for d in devices:

        log = BLELog(
            device_id=d["device_id"],
            rssi=d["rssi"],
            scanner_id=scanner_id
        )

        db.add(log)

        saved.append(log)

    db.commit()

    return saved