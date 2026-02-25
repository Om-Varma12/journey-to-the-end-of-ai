from typing import TypedDict, Optional, Dict, List

class State(TypedDict, total=False):
    repo_path: str
    username: str
    repo_name: str

    file_map: Dict                 # renamed from repo_structure

    # repo knowledge
    repo_summary: str
    dependencies: List[str]
    entry_points: List[str]
    language: str

    # per-file memory
    file_notes: Dict[str, Dict]    # summaries of important files

    # runtime interaction
    last_user_query: str
    target_file: str

    # metadata
    repo_details: Dict