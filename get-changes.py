import argparse
import yaml

parser = argparse.ArgumentParser(description="Find the changes since the last commit.")
parser.add_argument("--prev", type=str, required=True, help="Path to previous YAML revision")
parser.add_argument("--curr", type=str, required=True, help="Path to current YAML revision")

args = parser.parse_args()

with open(args.prev) as prev_file, open(args.curr) as curr_file:
    prev_data = yaml.safe_load(prev_file)
    curr_data = yaml.safe_load(curr_file)

    prev_namespaces = {ns["name"]: ns for ns in prev_data.get("namespaces", [])}
    curr_namespaces = {ns["name"]: ns for ns in curr_data.get("namespaces", [])}

    added_namespaces = [
        {"name": name, "region": curr_namespaces[name]["region"]}
        for name in curr_namespaces if name not in prev_namespaces
    ]

    removed_namespaces = [
        {"name": name, "region": prev_namespaces[name]["region"]}
        for name in prev_namespaces if name not in curr_namespaces
    ]

    import json
    print(f"::set-output name=added_namespaces::{json.dumps(added_namespaces)}")
    print(f"::set-output name=removed_namespaces::{json.dumps(removed_namespaces)}")
          