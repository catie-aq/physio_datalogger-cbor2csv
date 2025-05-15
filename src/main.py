import json

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
