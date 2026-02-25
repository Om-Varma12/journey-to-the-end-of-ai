from mcp.server.fastmcp import FastMCP
import subprocess
import os
import requests
from pathlib import Path
from pprint import pprint


BASE_DIR = "repos"

def register_repo_tools(mcp):
    print("Repo Tools Online")
    @mcp.tool()
    def clone_repo(username: str, repo_name: str) -> dict:
        """
        Clone a GitHub repository locally or pull the latest changes if it already exists.

        This tool ensures a local copy of the repository is available inside the `repos/`
        directory. If the repository has already been cloned earlier, it will perform
        a `git pull` to fetch the latest updates instead of cloning again.

        After cloning/pulling, the tool scans the repository and returns a structured
        overview of its contents for downstream agents to analyze.

        Args:
            username (str):
                GitHub username or organization name.

            repo_name (str):
                Name of the repository to clone.

        Returns:
            dict:
                {
                    "repo_path": str,        # local filesystem path of the repo
                    "repo_structure": {
                        "tree": dict,        # nested folder structure
                        "all_files": list,   # flat list of all files
                        "by_extension": dict,# files grouped by extension
                        "important_files": list # detected entry files
                    }
                }

        Notes:
            - Skips heavy/unnecessary folders like: node_modules, .git, dist, build.
            - Skips binary assets like images and lock files.
            - Designed to be idempotent for agent workflows.
            - Safe to call repeatedly in a multi-agent system.
        """
        os.makedirs(BASE_DIR, exist_ok=True)
        
        clone_url = f"https://github.com/{username}/{repo_name}.git"
        repo_path = os.path.join(BASE_DIR, repo_name)

        if os.path.exists(repo_path):
            print("Repo already cloned. Pulling latest changes...")
            subprocess.run(
                ["git", "-C", repo_path, "pull"],
                check=True
            )
        else:
            print("Cloning repo...")
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
    def get_repo_information(username: str, repo_name: str) -> dict:
        """
        Fetch basic metadata about a GitHub repository using the GitHub REST API.

        This tool retrieves high-level repository information such as description,
        primary language, creation date, and last update time. It does NOT clone
        the repository — it only queries GitHub's API.

        Useful for agents that need quick context before deciding whether to clone
        or analyze the repository.

        Args:
            username (str):
                GitHub username or organization name.

            repo_name (str):
                Repository name.

        Returns:
            dict:
                {
                    "description": str | None,
                    "language": str | None,
                    "created_at": str,          # ISO timestamp
                    "lasted_updated_at": str    # ISO timestamp
                }

        Raises:
            requests.HTTPError:
                If the repository does not exist or API rate limits are hit.

        Notes:
            - Uses GitHub public API (no auth).
            - Rate limit: ~60 requests/hour without token.
            - Can be extended to include stars, forks, topics, etc.
        """
        
        response = requests.get(f"https://api.github.com/repos/{username}/{repo_name}")
        info = response.json()
        

        return {
            "description": info['description'],
            "language": info['language'],
            "created_at": info['created_at'],
            "lasted_updated_at": info['updated_at']
        }