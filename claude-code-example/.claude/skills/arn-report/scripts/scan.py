"""Scan a file for ARNs and access key IDs and print the findings as JSON."""
import json
import re
import sys
from pathlib import Path

# Reuse the project's parser so the skill and the library never disagree.
sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from arn_utils import parse_arn  # noqa: E402

ARN_IN_TEXT = re.compile(r"arn:aws[a-z-]*:[^\s\"',]+")
KEY_IN_TEXT = re.compile(r"\bAKIA[A-Z0-9]{16}\b")


def scan(text: str) -> dict:
    arns = []
    for arn in sorted(set(ARN_IN_TEXT.findall(text))):
        try:
            arns.append({"arn": arn, **parse_arn(arn)})
        except ValueError:
            arns.append({"arn": arn, "error": "malformed ARN"})
    keys = [
        {"key": key, "is_example": key.endswith("EXAMPLE")}
        for key in sorted(set(KEY_IN_TEXT.findall(text)))
    ]
    return {"arns": arns, "access_key_ids": keys}


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: scan.py <file>")
    print(json.dumps(scan(Path(sys.argv[1]).read_text()), indent=2))
