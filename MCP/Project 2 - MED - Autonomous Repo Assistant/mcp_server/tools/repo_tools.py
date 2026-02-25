from mcp.server.fastmcp import FastMCP
import subprocess
import os

mcp = FastMCP("GH-REPO")

BASE_DIR = "repos"

@mcp.tool()
def clone_repo(username: str, repo_name: str) -> str:
    """Clones the github repository locally. 
    This tool is used when a user gives github repo to work with

    Args:
        username (str): username or the owner name
        repo_name (str): the actual repo name of the owner

    Returns:
        repo_path(str): return the repo path of clones repo
    """

    clone_url = f"https://github.com/{username}/{repo_name}.git"
    repo_path = os.path.join(BASE_DIR, repo_name)

    subprocess.run(
        ["git", "clone", clone_url, repo_path],
        check=True
    )

    return repo_path

# clone_repo("Om-Varma12", "PaperForge")