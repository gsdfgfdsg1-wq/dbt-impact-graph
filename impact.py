#!/usr/bin/env python3
"""Compute dbt model downstream impact and data-quality gaps."""
import argparse
import json
from collections import defaultdict
from pathlib import Path


def analyze(models, changed=None):
    downstream = defaultdict(set)
    names = {model["name"] for model in models}
    for model in models:
        for parent in model.get("depends_on", []): downstream[parent].add(model["name"])
    impacted = set()
    def visit(node):
        for child in downstream[node]:
            if child not in impacted: impacted.add(child); visit(child)
    if changed: visit(changed)
    untested = sorted(model["name"] for model in models if not model.get("tests"))
    isolated = sorted(model["name"] for model in models if not model.get("depends_on") and not downstream[model["name"]])
    return {"changed": changed, "impacted": sorted(impacted), "rerun": [changed] + sorted(impacted) if changed else [], "untested": untested, "isolated": isolated, "models": sorted(names)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("models"); parser.add_argument("--changed")
    args = parser.parse_args()
    print(json.dumps(analyze(json.loads(Path(args.models).read_text()), args.changed), indent=2))


if __name__ == "__main__":
    main()
