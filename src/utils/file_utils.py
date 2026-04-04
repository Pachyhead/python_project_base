import os
from pathlib import Path

from config import PROJECT_ROOT

def get_file_iterator(directory_path: str=os.path.join(PROJECT_ROOT, "source"), extension: str = ""):
    """
    read the directory and get the file iterator
    default directory is project/source
    """
    path = Path(directory_path)
    if extension == "":
        for file_path in path.glob("*"):
            if file_path.is_file():
                yield file_path
    else:
        for file_path in path.glob(f"*.{extension}"):
            if file_path.is_file():
                yield file_path