import subprocess
import os
import requests
from pathlib import Path


BASE_DIR = "repos"

def check_repo_exist(repo_name: str) -> bool:
    repo_path = BASE_DIR + '/' + repo_name
    return True if(os.path.exists(repo_path)) else False

def clone_repo(username: str, repo_name: str) -> dict:
    os.makedirs(BASE_DIR, exist_ok=True)
    
    clone_url = f"https://github.com/{username}/{repo_name}.git"
    repo_path = BASE_DIR + '/' + repo_name
    
    subprocess.run(
        ["git", "clone", clone_url, repo_path],
        check=True
    )

def get_repo_structure(repo_name):
    repo_path = Path(BASE_DIR) / repo_name   # Proper Path object
    root_path = repo_path 

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

    return file_map
    
def pull_latest_changes(repo_name: str) -> bool:
    repo_path = BASE_DIR + '/' + repo_name
    if(os.path.exists(repo_path)):
        subprocess.run(
            ["git", "-C", repo_path, "pull"],
            check=True
        )
        return True
    else:
        return False

def get_repo_details(username: str, repo_name: str):
    url = f'https://api.github.com/repos/{username}/{repo_name}'
    response = requests.get(url)
    data = response.json()
    return {
        'repo_description': data['description'],
        'repo_language': data['language']
    }