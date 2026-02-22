# add_server.py
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("add_server")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

if __name__ == "__main__":
    mcp.run(transport="stdio") # stdio transport