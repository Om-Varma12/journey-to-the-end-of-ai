from mcp.server.fastmcp import FastMCP
import os

mcp = FastMCP("FileSystem")
ROOT_DIR = os.getcwd()

@mcp.tool()
def set_folder_location(path: str):
    """Set working directory for file operations        

    Args:
        location (str): location of the folder
    """
    global ROOT_DIR         ## accessing the global variable in function

    if not os.path.isdir(path):
        return "Invalid directory"

    ROOT_DIR = path
    return f"Root folder set to {ROOT_DIR}"

@mcp.tool()
def list_files() -> list:
    """ALWAYS call this tool to list files in the current directory.
    Never guess or reuse previous results.
    The filesystem may have changed."""
    try:
        return os.listdir(ROOT_DIR)
    
    except Exception as e:
        return [f"Error: {str(e)}"]
    
@mcp.tool()
def read_file(filename: str) -> str:
    """Read file from root directory"""
    try:
        full_path = os.path.join(ROOT_DIR, filename)
        
        with open(full_path, "r", encoding="utf-8") as f:
            return f.read()
        
    except Exception as e:
        return f"Error: {str(e)}"
    
@mcp.tool()
def write_file(filename: str, content: str) -> str:
    """Write file to root directory"""
    try:
        full_path = os.path.join(ROOT_DIR, filename)
        
        with open(full_path, "w") as f:
            f.write(content)
            
        return "File written successfully"
    
    except Exception as e:
        return f"Error: {str(e)}"
    
if __name__ == "__main__":
    mcp.run()
    # no transport specified = 'stdio' by default