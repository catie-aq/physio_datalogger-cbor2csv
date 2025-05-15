import json
import pprint

config_path = "config/config.json"
output = []

# Load json
with open(config_path, "r", encoding="utf-8") as file:
    config = json.load(file)

for device in config["devices"]:
    device_name = device["name"]
    
    for frame in device["communication"]["frames"]:
        frame_size = frame["size"]
        for field in frame["data"]:
            entry = {
                "device": device_name,
                "field": field["name"],
                "msb": field["msb"],
                "lsb": field["lsb"],
                "bytes_used": abs(field["msb"] - field["lsb"]) + 1,
                "endianness": "big" if field["msb"] > field["lsb"] else "little",
                "valid_range": field["msb"] < frame_size and field["lsb"] < frame_size
            }
            output.append(entry)

# Display 
print("Configuration input:\n")
pprint.pprint(output)