"""A custom tool for Claude Code, served over MCP (registered in ../.mcp.json).

TOOL DESIGN (exam concepts):
  - The docstring IS the tool description Claude reads to decide when to call it,
    so it says what the tool does, what it returns, and when NOT to use it.
  - Failures come back as structured errors (category + retryable flag) instead of a
    bare "error" string, so Claude can tell "fix your input" from "try again later".
"""
import sys
from pathlib import Path

from mcp.server.mcpserver import MCPServer  # mcp>=2 (called FastMCP in mcp 1.x)

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from arn_utils import is_valid_access_key_id, parse_arn  # noqa: E402

mcp = MCPServer("arn-tools")


@mcp.tool()
def lookup_arn(arn: str) -> dict:
    """Parse ONE AWS ARN into partition, service, region, account and resource.

    Use this to answer questions about a single ARN (which region, which account).
    An empty region means a global resource such as IAM or an S3 bucket.
    To inventory many ARNs in a file, use the arn-report skill instead.
    """
    try:
        return {"isError": False, **parse_arn(arn)}
    except ValueError as exc:
        return {
            "isError": True,
            "errorCategory": "validation",
            "isRetryable": False,
            "message": f"{exc}. Expected arn:partition:service:region:account-id:resource",
        }


@mcp.tool()
def check_access_key_id(key_id: str) -> dict:
    """Check whether a string has the format of a long-term AWS access key ID (AKIA + 16 chars).

    This only checks the FORMAT; it never contacts AWS and cannot tell if a key is active.
    """
    return {
        "isError": False,
        "valid_format": is_valid_access_key_id(key_id),
        "is_documentation_example": key_id.endswith("EXAMPLE"),
    }


if __name__ == "__main__":
    mcp.run()  # stdio transport: Claude Code starts this process and talks over stdin/stdout
