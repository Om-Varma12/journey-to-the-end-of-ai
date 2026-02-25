from typing import TypedDict

class State(TypedDict):
    repo_path: str
    repo_summary: str
    current_target_file: str
    main_entry_point: str