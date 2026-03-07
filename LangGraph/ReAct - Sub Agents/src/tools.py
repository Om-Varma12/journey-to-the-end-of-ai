from langchain_core.tools import tool

file_system = {}

@tool
def write_file(path: str, content: str):
    """
    Write content to a file path inside the virtual project filesystem.
    """
    file_system[path] = content
    return f"File {path} written successfully."

@tool
def read_file(path: str):
    """
    Read content from a file path in the project filesystem.
    """
    if path not in file_system:
        return "File does not exist."
    return file_system[path]

@tool
def list_files():
    """
    List all files currently in the project filesystem.
    """
    return list(file_system.keys())