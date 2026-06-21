# Telemetry Data Format Converter

This repository contains a Python 3 project that converts telemetry records from two input formats into a unified JSON structure.

## Files

- `data-1.json`: sample input using Format 1
- `data-2.json`: sample input using Format 2
- `data-result.json`: expected unified output for `data-1.json`
- `main.py`: converter implementation and unit tests

## Usage

Run the project with:

```bash
python main.py
```

This executes the unit tests and prints converted JSON output for the sample files.

## Conversion functions

- `convertFromFormat1(jsonObject)` converts Format 1 into the unified structure
- `convertFromFormat2(jsonObject)` converts Format 2 and normalizes the ISO-8601 timestamp to milliseconds since epoch

## Testing

The project uses Python's built-in `unittest` framework. The included tests verify:

- sanity check
- conversion from Format 1
- conversion from Format 2
