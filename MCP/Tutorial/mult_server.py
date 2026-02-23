# multiply_server.py
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("multiply_server")

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b

if __name__ == "__main__":
    mcp.run(transport="stdio")  # stdio transport