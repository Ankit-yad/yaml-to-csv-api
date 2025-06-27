import yaml
import csv
import io

def flatten(d, parent_key='', sep='.'):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten(v, new_key, sep=sep).items())
        elif isinstance(v, list):
            if all(isinstance(i, dict) for i in v):
                for index, item in enumerate(v):
                    items.extend(flatten(item, f"{new_key}[{index}]", sep=sep).items())
            else:
                items.append((new_key, str(v)))
        else:
            items.append((new_key, v))
    return dict(items)

def yaml_to_csv_stream(yaml_content: str) -> io.BytesIO:
    data = list(yaml.safe_load_all(yaml_content))

    flat_data = []
    for item in data:
        if isinstance(item, dict):
            flat_data.append(flatten(item))
        elif isinstance(item, list):
            flat_data.extend(flatten(i) for i in item if isinstance(i, dict))

    if not flat_data:
        raise ValueError("No valid data found in YAML.")

    headers = sorted(set().union(*(row.keys() for row in flat_data)))

    csv_stream = io.StringIO()
    writer = csv.DictWriter(csv_stream, fieldnames=headers, quoting=csv.QUOTE_ALL)
    writer.writeheader()
    writer.writerows(flat_data)

    result = io.BytesIO()
    result.write(csv_stream.getvalue().encode())
    result.seek(0)
    return result
