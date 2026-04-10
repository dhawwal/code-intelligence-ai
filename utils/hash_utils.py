import hashlib

def generate_repo_id(repo_url: str) -> str:
    """
    Generates an MD5 hash of the repository URL to use as a unique ID.
    """
    # Normalize the URL by stripping trailing slashes and .git suffix
    normalized = repo_url.strip().rstrip('/')
    if normalized.endswith('.git'):
        normalized = normalized[:-4]
        
    return hashlib.md5(normalized.encode('utf-8')).hexdigest()
