import os
from typing import List

SUPPORTED_EXTENSIONS = {".py", ".js", ".ts", ".tsx", ".java"}

def get_code_files(repo_path: str) -> List[str]:
    """
    Recursively fetch all source code files that match the supported extensions.
    """
    file_paths = []
    for root, dirs, files in os.walk(repo_path):
        # Ignore `.git` and `node_modules` completely
        if '.git' in dirs:
            dirs.remove('.git')
        if 'node_modules' in dirs:
            dirs.remove('node_modules')
        if 'venv' in dirs:
            dirs.remove('venv')
            
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in SUPPORTED_EXTENSIONS:
                file_paths.append(os.path.join(root, file))
                
    return file_paths
