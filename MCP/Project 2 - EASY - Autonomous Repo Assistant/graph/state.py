from typing import TypedDict, Optional, List, Dict

class State(TypedDict, total=False):
    # repo identity
    username: str
    repo_name: str

    # repo data
    repo_path: Optional[str]
    repo_structure: Optional[Dict]
    repo_details: dict

    # runtime
    user_question: str
    relevant_files: Optional[List[str]]
    repo_summary: Optional[str]

    # routing
    next_node: Optional[str]
    sub_next_node: Optional[str]  

    # output
    final_answer: Optional[str]
    
    # file related state
    current_file: Optional[str]
    file_cache: Dict[str, str]