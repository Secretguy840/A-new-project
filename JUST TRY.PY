import os
import requests

def get_repos(platform, username, token=None):
    """
    Fetch all repositories for a given user/organization from GitHub or GitLab.
    """
    repos = []
    if platform == "github":
        url = f"https://api.github.com/users/Secretguy840/repos" if not token else f"https://api.github.com/orgs/Secretguy840/repos"
        headers = {"Authorization": f"token {token}"} if token else {}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            repos = [repo["clone_url"] for repo in response.json()]
        else:
            print(f"Error fetching GitHub repos: {response.status_code}")
    elif platform == "gitlab":
        url = f"https://gitlab.com/api/v4/users/Secretguy840/projects"
        headers = {"Private-Token": token} if token else {}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            repos = [repo["http_url_to_repo"] for repo in response.json()]
        else:
            print(f"Error fetching GitLab repos: {response.status_code}")
    else:
        print("Unsupported platform. Use 'github' or 'gitlab'.")
    return repos

def clone_repos(repos, target_dir="repos"):
    """
    Clone all repositories into a target directory.
    """
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    for repo in repos:
        repo_name = repo.split("/")[-1].replace(".git", "")
        repo_dir = os.path.join(target_dir, repo_name)
        if not os.path.exists(repo_dir):
            print(f"Cloning {repo_name}...")
            os.system(f"git clone {repo} {repo_dir}")
        else:
            print(f"Skipping {repo_name} (already exists).")

if __name__ == "__main__":
    # Configuration
    PLATFORM = "github"
    USERNAME = "Secretguy840"
    TOKEN = "your_personal_access_token"  # Optional, for private repos
    TARGET_DIR = "repos"  # Directory to clone repositories into

    # Fetch and clone repositories
    repos = get_repos(PLATFORM, USERNAME, TOKEN)
    if repos:
        clone_repos(repos, TARGET_DIR)
    else:
        print("No repositories found or an error occurred.")
