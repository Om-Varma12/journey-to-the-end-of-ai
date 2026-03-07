from pathlib import Path

BASE_REPO_DIR = "repos"

def read_file_content(repo_name: str, file_path: str) -> str:
    full_path = Path(BASE_REPO_DIR) / repo_name / file_path

    if not full_path.exists():
        raise FileNotFoundError(f"{file_path} not found.")

    return full_path.read_text(encoding="utf-8")