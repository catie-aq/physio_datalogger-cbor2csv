import json

config_path = "config/config.json"

with open(config_path, "r", encoding="utf-8") as file:
    config = json.load(file)

print("Configuration input:")
for key, value in config.items():
    print(f"{key} : {value}\n")
