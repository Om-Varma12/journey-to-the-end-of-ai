from mcp.server.fastmcp import FastMCP
import subprocess
import os
import requests
from pathlib import Path
from pprint import pprint

mcp = FastMCP("GH-REPO")

BASE_DIR = "repos"

@mcp.tool()
def clone_repo(username: str, repo_name: str) -> dict:
    clone_url = f"https://github.com/{username}/{repo_name}.git"
    repo_path = os.path.join(BASE_DIR, repo_name)

    subprocess.run(
        ["git", "clone", clone_url, repo_path],
        check=True
    )

    root_path = Path(repo_path)

    file_map = {
        "tree": {},
        "all_files": [],
        "by_extension": {},
        "important_files": []
    }

    imp_file = ["main.py", "app.py", "main.html", "index.js", "README.md", "package.json", "App.tsx", "main.tsx"]

    for path in root_path.rglob("*"):
        if not path.is_file():
            continue

        if any(x in path.parts for x in ["node_modules", ".git", "__pycache__", "dist", "build"]):
            continue

        if path.suffix in [".lock", ".png", ".jpg", ".svg", ".pack"]:
            continue

        relative_path = path.relative_to(root_path)
        relative_str = str(relative_path).replace("\\", "/")

        # all files
        file_map["all_files"].append(relative_str)

        # by extension
        ext = path.suffix or "no_extension"
        file_map["by_extension"].setdefault(ext, []).append(relative_str)

        # important files
        if path.name in imp_file:
            file_map["important_files"].append(relative_str)

        # tree build
        parts = relative_path.parts
        current = file_map["tree"]

        for part in parts[:-1]:
            current = current.setdefault(part, {})

        current[parts[-1]] = {}

    return {
        "repo_path": repo_path,
        "repo_structure": file_map
    }
    
    
pprint(clone_repo("Om-Varma12", "CrackEM"))

@mcp.tool()
def get_repo_information(username: str, repo_name: str) -> dict:
    """Get the Repository Information

    Args:
        username (str): GitHub username
        repo_name (str): Repository name

    Returns:
        dict: information of repository in json format
    """
    
    response = requests.get(f"https://api.github.com/repos/{username}/{repo_name}")
    info = response.json()
    

    return {
        "description": info['description'],
        "language": info['language'],
        "created_at": info['created_at'],
        "lasted_updated_at": info['updated_at']
    }
    
# pprint(get_repo_information("Om-Varma12", "PaperForge"))