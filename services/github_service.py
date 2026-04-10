import os
from git import Repo
from config import Config

def clone_or_pull_repo(repo_url: str, repo_id: str) -> str:
    """
    Clones the repository if it doesn't exist, else performs a git pull.
    Returns the absolute path to the repository directory.
    """
    repo_path = os.path.join(Config.REPOS_DIR, repo_id)
    
    if os.path.exists(repo_path) and os.path.exists(os.path.join(repo_path, ".git")):
        print(f"Repository {repo_id} exists. Pulling latest changes...")
        repo = Repo(repo_path)
        origin = repo.remotes.origin
        origin.pull()
    else:
        print(f"Cloning {repo_url} into {repo_path} (shallow, blobless)...")
        # Shallow and blobless clone for maximum speed
        Repo.clone_from(repo_url, repo_path, depth=1, multi_options=["--filter=blob:none"])
        
    return repo_path
