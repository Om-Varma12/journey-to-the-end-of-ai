# weather_server.py
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("weather_server")

@mcp.tool()
async def get_weather(location: str) -> str:
    """Get current weather for a location"""
    return f"Weather in {location}: rainy"

if __name__ == "__main__":
    mcp.run(transport="streamable-http")