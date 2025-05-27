import json
import csv
from cbor2 import CBORDecoder
from pathlib import Path


def iterdecode(f):
    decoder = CBORDecoder(f)
    while True:
        try:
            yield decoder.decode()
        except EOFError:
            return


def main():
    print("Physio Datalogger is running!")

    CONFIG_PATH = Path("config/config.json")
    CBOR_PATH = Path("data/Z_Motion_2026-01-14_21-52-32.cbor")
    CSV_PATH = Path("output") / f"{CBOR_PATH.stem}_result.csv"

    with CONFIG_PATH.open("r", encoding="utf-8") as f:
        config = json.load(f)

    device_name = "_".join(CBOR_PATH.name.split("_")[0:-2])
    device_config = next(dev for dev in config["devices"] if dev["name"] == device_name)

    fields = []
    for frame in device_config["communication"]["frames"]:
        for entry in frame["data"]:
            fields.append((entry["name"], entry["msb"], entry["lsb"]))

    decoded_rows = []
    with CBOR_PATH.open("rb") as fp:
        for obj in iterdecode(fp):
            if not isinstance(obj, list) or len(obj) != 2:
                continue
            _, raw = obj
            if not isinstance(raw, bytes) or len(raw) != 20:
                continue

            for i in range(0, 20, 10):
                frame = raw[i : i + 10]
                row = {}
                buffer = bytearray(frame)

                for name, msb, lsb in fields:
                    start = min(msb, lsb)
                    end = max(msb, lsb)
                    if end >= len(buffer):
                        break
                    if start == end:
                        val = (
                            buffer[start]
                            if buffer[start] < 128
                            else buffer[start] - 256
                        )
                    else:
                        val = int.from_bytes(
                            buffer[start : end + 1], byteorder="little", signed=True
                        )
                    row[name] = val

                if "timestamp" in row:
                    decoded_rows.append(row)

    fieldnames = [name for name, _, _ in fields]
    with CSV_PATH.open("w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in decoded_rows:
            writer.writerow(row)

    print(f"Data exported to: {CSV_PATH}")
