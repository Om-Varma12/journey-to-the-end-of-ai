from mcp.server.fastmcp import FastMCP

from tools.file_tools import register_file_tools

mcp = FastMCP("autonomous-repo-assistant")

# Register all tool groups
register_file_tools(mcp)

if __name__ == "__main__":
    mcp.run()