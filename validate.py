import argparse
import yaml
import sys

ALLOWED_REGIONS = ["ap-southeast-2", "us-east-1"]

parser = argparse.ArgumentParser(description="Simple validation of Temporal.yaml")
parser.add_argument("--input", type=str, required=True, help="Path to Temporal YAML")

args = parser.parse_args()

with open(args.input) as input_file:
    input_data = yaml.safe_load(input_file)

    # Namespaces
    raw_namespaces = input_data.get("namespaces", [])
    namespaces = {}

    for namespace in raw_namespaces:
        if namespace["name"] in namespaces:
            print(f"Duplicate namespace: {namespace["name"]}")
            sys.exit(1)

        if namespace["region"] not in ALLOWED_REGIONS:
            print(f"Invalid region: {namespace["region"]}")
            sys.exit(1)

        namespaces[namespace["name"]] = namespace

print("Valid")