import os
import httpx

class GitHubClient:
    def __init__(self):
        # 1. Load the token from the environment
        # If you are still getting errors, you can temporarily hardcode it here:
        # self.token = "ghp_your_real_token_here"
        self.token = os.getenv("GITHUB_TOKEN")
        
        # 2. Define the Base URL immediately
        self.base_url = "https://api.github.com"
        
        # 3. Define the Headers
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28"
        }
        
        print(f"DEBUG: GitHubClient initialized with base_url: {self.base_url}")

    async def get_org_repos(self, org: str, include_private: bool):
        """Fetches repositories for the organization."""
        repo_type = "all" if include_private else "public"
        
        # This is where your error was happening
        url = f"{self.base_url}/orgs/{org}/repos?type={repo_type}&per_page=100"
        
        print(f"DEBUG: Fetching repos from: {url}")
        
        async with httpx.AsyncClient(headers=self.headers, timeout=30.0) as client:
            resp = await client.get(url)
            if resp.status_code != 200:
                print(f"DEBUG: GitHub Repos API failed: {resp.status_code} - {resp.text}")
                return []
            return resp.json()

    async def get_repo_collaborators(self, org: str, repo: str):
        """Fetches collaborators for a specific repository."""
        if not repo:
            return []
            
        url = f"{self.base_url}/repos/{org}/{repo}/collaborators?per_page=100"
        
        async with httpx.AsyncClient(headers=self.headers, timeout=30.0) as client:
            resp = await client.get(url)
            if resp.status_code == 200:
                return resp.json()
            return []