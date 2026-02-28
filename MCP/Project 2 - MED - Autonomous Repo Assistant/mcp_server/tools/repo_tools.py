from mcp.server.fastmcp import FastMCP
import subprocess
import os
import requests
from pathlib import Path
from pprint import pprint


BASE_DIR = "repos"

def register_repo_tools(mcp):
    # print("Repo Tools Online")
    @mcp.tool()
    def check_repo_exist(repo_name: str) -> bool:
        """
        Check whether a repository is already cloned locally.

        Args:
            repo_name (str): Name of the repository directory inside the BASE_DIR.

        Returns:
            bool: 
                - True if the repository folder exists locally.
                - False if the repository is not found.

        Notes:
            - This function only checks for directory existence.
            - It does NOT verify whether the directory is a valid git repository.
            - No network or git operations are performed.
        """
        repo_path = BASE_DIR + '/' + repo_name
        return True if(os.path.exists(repo_path)) else False
    
    
    @mcp.tool()
    def clone_repo(username: str, repo_name: str) -> dict:
        """
        Clone a GitHub repository locally and generate a structured file map.

        Args:
            username (str): GitHub username or organization name.
            repo_name (str): Name of the GitHub repository.

        Returns:
            dict: A dictionary containing:
                - "repo_path" (str): Local filesystem path where the repo was cloned.
                - "repo_structure" (dict):
                    - "tree": Nested dictionary representing folder structure.
                    - "all_files": List of all relevant file paths (relative).
                    - "by_extension": Dictionary grouping files by file extension.
                    - "important_files": List of key entry-point files detected 
                    (e.g., main.py, app.py, README.md, package.json, etc.).

        Behavior:
            - Clones the repository using `git clone`.
            - Skips irrelevant directories:
                node_modules, .git, __pycache__, dist, build, __init__.py
            - Skips binary/irrelevant file types:
                .lock, .png, .jpg, .svg, .pack
            - Builds a structured representation for intelligent repo analysis.

        Raises:
            subprocess.CalledProcessError:
                If git clone fails (invalid repo, network issue, etc.).

        Side Effects:
            - Creates BASE_DIR if it does not exist.
            - Downloads repository contents to local filesystem.
        """
        os.makedirs(BASE_DIR, exist_ok=True)
        
        clone_url = f"https://github.com/{username}/{repo_name}.git"
        repo_path = BASE_DIR + '/' + repo_name
        
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

            if any(x in path.parts for x in ["node_modules", ".git", "__pycache__", "dist", "build", "__init__.py"]):
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
        
    @mcp.tool()
    def pull_latest_changes(repo_name: str) -> bool:
        """
        Pull the latest changes from the remote repository.

        Args:
            repo_name (str): Name of the locally cloned repository.

        Returns:
            bool:
                - True if the repository exists and pull was successful.
                - False if the repository directory does not exist.

        Behavior:
            - Executes `git pull` inside the repository directory.
            - Does not handle merge conflicts explicitly.
            - Assumes the repository has a valid remote origin.

        Raises:
            subprocess.CalledProcessError:
                If git pull fails due to network issues or git errors.

        Side Effects:
            - Updates local repository files.
        """
        repo_path = BASE_DIR + '/' + repo_name
        if(os.path.exists(repo_path)):
            subprocess.run(
                ["git", "-C", repo_path, "pull"],
                check=True
            )
            return True
        else:
            return False
    