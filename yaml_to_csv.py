import yaml
import csv
import sys

# Recursive function to flatten nested dictionaries
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

def yaml_to_csv(yaml_file, csv_file):
    with open(yaml_file, 'r') as yf:
        data = list(yaml.safe_load_all(yf))


    # Always convert to a list of one or more flat dictionaries
    if isinstance(data, dict):
        data = [flatten(data)]
    elif isinstance(data, list):
        data = [flatten(item) for item in data]
    else:
        print("Unsupported YAML structure.")
        return

    # Write to CSV
    with open(csv_file, 'w', newline='') as cf:
        headers = set()
        for row in data:
            headers.update(row.keys())
        headers = sorted(headers)
        writer = csv.DictWriter(cf, fieldnames=headers, quoting=csv.QUOTE_ALL)

        writer.writeheader()
        writer.writerows(data)

    print(f"CSV file created successfully at: {csv_file}")

if __name__ == "__main__":
    yaml_to_csv('data.yml','yaml_to_csv.csv')
