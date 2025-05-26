import json
from cbor2 import CBORDecoder

CONFIG_PATH = "config/config.json"
CBOR_PATH = "data/Z_Motion_2026-01-19_10-48-03.cbor"
#CBOR_PATH = "data/AFE4960_03_2026-01-12_20-10-50.cbor"

with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    config = json.load(f)

print(f"CBOR: {CBOR_PATH} | SPLIT:{'_'.join(CBOR_PATH.split('/')[-1].split('_')[0:-2])}")
config = next(dev for dev in config["devices"] if dev["name"] == '_'.join(CBOR_PATH.split('/')[-1].split('_')[0:-2]))
fields = []
for frame in config["communication"]["frames"]:
    for entry in frame["data"]:
        print(entry)
        fields.append((entry["name"], entry["msb"], entry["lsb"]))

# Print the fields
print("Fields:")
for field in fields:
    print(f"  {field[0]}: msb={field[1]}, lsb={field[2]}")

# print quantities
print("Quantities:")
print(f"  {frame['quantity']}")

# print size
print("Size:")
print(f"  {frame['size']}")

data_dict = {}
frame_count = 0 

def iterdecode(f):
    decoder = CBORDecoder(f)
    while True:
        try:
            yield decoder.decode()
        except EOFError:
            return

with open(CBOR_PATH, "rb") as fp:
    for obj in iterdecode(fp):

        if not isinstance(obj, list) or len(obj) != 2:
            print(f"Invalid frame: {obj}")
            continue

        timestamp, raw = obj
        if not isinstance(raw, bytes):
            print(f"Non-binary data: {raw}")
            continue

        if not isinstance(timestamp, int):
            print(f"Invalid timestamp: {timestamp}")
            continue

        row = {"timestamp": timestamp}
        buffer = bytearray(raw)

        for name, msb, lsb in fields:
            start = min(msb, lsb)
            end = max(msb, lsb)

            if end >= len(buffer):
                print(f"Frame too short (length={len(buffer)}): {[timestamp, raw]}")
                break  
            if start == end:
                val = buffer[start] if buffer[start] < 128 else buffer[start] - 256
            else:
                val = int.from_bytes(buffer[start:end+1], byteorder="little", signed=True)

            row[name] = val

        else:
            data_dict[timestamp] = row
            frame_count += 1  

print(f"Frames: {frame_count}")