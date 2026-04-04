import json
import os
from pathlib import Path

from config import PROJECT_ROOT

def get_json_file_iterator(directory_path: str=os.path.join(PROJECT_ROOT, "source")):
    """
    read the directory and get the json file iterator
    default directory is project/source
    """
    path = Path(directory_path)
    for file_path in path.glob(f"*.json"):
        with open(file_path, 'r', encoding='utf-8') as f:
            yield json.load(f)

def get_file_iterator(directory_path: str = os.path.join(PROJECT_ROOT, "source")):
    """
    Find files only in the current level.
    """
    path = Path(directory_path)
    
    for file_path in path.glob("*"):
        if file_path.is_file():
            yield file_path
