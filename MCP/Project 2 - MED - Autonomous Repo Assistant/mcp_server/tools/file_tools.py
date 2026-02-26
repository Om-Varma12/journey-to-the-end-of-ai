from mcp.server.fastmcp import FastMCP
import os

def register_file_tools(mcp):
    print("File Tools Online")
    @mcp.tool()
    def get_file(repo_name: str, file_path: str) -> str:
        """
        Read and return the contents of a file from a locally cloned repository.

        This tool is used by agents to access specific files inside repositories
        that were previously cloned into the `repos/` directory. It constructs the
        absolute path using the repository name and the relative file path, then
        returns the file's text content.

        Args:
            repo_name (str):
                Name of the repository folder inside the local `repos/` directory.

            file_path (str):
                Relative path to the target file inside the repository.
                Example: "src/main.py" or "ai/prompts/starterAgent.txt"

        Returns:
            str:
                Full text content of the requested file.

        Raises:
            FileNotFoundError:
                If the repository or file path does not exist.

            UnicodeDecodeError:
                If the file is not a readable text file.

        Notes:
            - Assumes repository has already been cloned locally.
            - Intended for text/code files only.
            - Should not be used for large binaries.
            - Core tool for repo-analysis agents to read source files.
        """
        final_path = "repos/" + repo_name + "/" + file_path
        with open(final_path, "r") as f:
            content = f.read()
        
        return(content)
        
    # get_file("CrackEM", "ai/prompts/starterAgent.txt")