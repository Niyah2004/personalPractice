"""Small AWS helper functions. This is the "codebase" Claude works on in the example."""
import re

# arn:partition:service:region:account-id:resource
ARN_PATTERN = re.compile(
    r"^arn:(?P<partition>aws[a-z-]*):(?P<service>[a-z0-9-]+):"
    r"(?P<region>[a-z0-9-]*):(?P<account>\d{12}|):(?P<resource>.+)$"
)
ACCESS_KEY_ID_PATTERN = re.compile(r"^AKIA[A-Z0-9]{16}$")


def parse_arn(arn: str) -> dict:
    """Split an ARN into its parts. Raises ValueError if it is not a valid ARN."""
    match = ARN_PATTERN.match(arn.strip())
    if not match:
        raise ValueError(f"Not a valid ARN: {arn!r}")
    return match.groupdict()


def extract_region(arn: str):
    """Return the region of an ARN, or None for global resources (e.g. S3 buckets, IAM)."""
    return parse_arn(arn)["region"] or None


def is_valid_access_key_id(key_id: str) -> bool:
    """True if the string looks like a long-term AWS access key ID (AKIA + 16 chars)."""
    return bool(ACCESS_KEY_ID_PATTERN.match(key_id))
