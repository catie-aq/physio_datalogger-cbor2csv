# physio_datalogger-cbor2csv

CBOR TO CSV is a tool designed to convert CBOR (Concise Binary Object Representation) data into CSV format.

Additional line of information text about what the project does.

## Prerequisites

Before you begin, ensure you have met the following requirements:

## Installing physio_datalogger-cbor2csv

To install physio_datalogger-cbor2csv, follow these steps:

```bash
poetry install
```

This will install all dependencies in a virtual environment managed by Poetry.

## Using physio_datalogger-cbor2csv

To use physio_datalogger-cbor2csv, follow these steps:

1. Ensure you have the following files:
   - A CBOR file containing the binary data (e.g., `data/Z_Motion_2026-01-14_21-52-32.cbor`).
   - A configuration JSON file specifying the device structure (e.g., `config/config.json`).

2. Run the following command to convert the CBOR file to CSV:

```bash
poetry run physio_datalogger --input <path_to_cbor_file> --config <path_to_config_file> --output <path_to_output_csv>
```

For example:

```bash
poetry run physio_datalogger --input data/Z_Motion_2026-01-14_21-52-32.cbor --config config/config.json --output result.csv
```

3. The output CSV file will be saved at the location specified by the `--output` option.

## License

This project is licensed under Apache 2.0, a permissive open source license that
allows you to freely use, modify, distribute, and sell your own
products that include this software. The full text of the license can be
obtained from the [Apache website](https://www.apache.org/licenses/LICENSE-2.0).
