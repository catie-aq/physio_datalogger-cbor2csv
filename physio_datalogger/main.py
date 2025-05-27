import click
import json
import csv
from pathlib import Path
from cbor2 import CBORDecoder


def iterdecode(f):
    decoder = CBORDecoder(f)
    while True:
        try:
            yield decoder.decode()
        except EOFError:
            return


@click.command()
@click.option(
    "--input",
    "input_path",
    required=True,
    type=click.Path(exists=True),
    help="Input CBOR file",
)
@click.option(
    "--config",
    "config_path",
    required=True,
    type=click.Path(exists=True),
    help="Device config JSON file",
)
@click.option(
    "--output",
    "output_path",
    required=True,
    type=click.Path(),
    help="Output CSV file",
)
def main(input_path, config_path, output_path):
    input_path = Path(input_path)
    config_path = Path(config_path)
    output_path = Path(output_path)

    with config_path.open("r", encoding="utf-8") as f:
        config = json.load(f)

    device_name = "_".join(input_path.name.split("_")[0:-2])
    device_config = next(dev for dev in config["devices"] if dev["name"] == device_name)

    fields = [
        (entry["name"], entry["msb"], entry["lsb"])
        for frame in device_config["communication"]["frames"]
        for entry in frame["data"]
    ]

    decoded_rows = []
    with input_path.open("rb") as fp:
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
                    start, end = min(msb, lsb), max(msb, lsb)
                    if end >= len(buffer):
                        break
                    val = (
                        buffer[start]
                        if start == end
                        else int.from_bytes(
                            buffer[start : end + 1], byteorder="little", signed=True
                        )
                    )
                    row[name] = val

                if "timestamp" in row:
                    decoded_rows.append(row)

    fieldnames = [name for name, _, _ in fields]
    with output_path.open("w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(decoded_rows)

    click.echo(f" Data exported to {output_path}")
