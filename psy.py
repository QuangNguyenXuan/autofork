import requests
import time

# GitHub credentials
SOURCE_USER = "XXX"
TARGET_USER = "XXX"
GITHUB_TOKEN = "XXX"

# GitHub API URLs
GITHUB_API = "https://api.github.com"
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}

def get_repos(user):
    """Fetch all repositories of a user."""
    repos = []
    page = 1
    while True:
        url = f"{GITHUB_API}/users/{user}/repos?page={page}&per_page=100"
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            print("Error fetching repositories:", response.json())
            break
        data = response.json()
        if not data:
            break
        repos.extend(data)
        page += 1
    return repos

def fork_repo(repo_full_name):
    """Fork a repository with retry logic and delay."""
    url = f"{GITHUB_API}/repos/{repo_full_name}/forks"

    for attempt in range(3):  # Retry up to 3 times
        response = requests.post(url, headers=HEADERS)

        if response.status_code == 202:
            print(f"✅ Forked: {repo_full_name}")
            time.sleep(10)  # 10-second delay to prevent rate limits
            return True  # Success

        elif response.status_code == 403 and "was submitted too quickly" in response.text:
            print(f"⚠️ Rate limit hit! Waiting before retrying {repo_full_name}...")
            time.sleep(30)  # Wait 30 seconds before retrying

        else:
            print(f"❌ Failed to fork {repo_full_name}: {response.json()}")
            return False  # Failure

    return False  # Failed after retries

if __name__ == "__main__":
    print("Fetching repositories from:", SOURCE_USER)
    repos = get_repos(SOURCE_USER)

    if not repos:
        print("No repositories found.")
    else:
        print(f"Found {len(repos)} repositories. Forking now...")
        for repo in repos:
            fork_repo(repo["full_name"])

    print("✅ All repositories processed!") 
