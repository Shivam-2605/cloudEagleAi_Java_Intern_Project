import asyncio
from app.github.client import GitHubClient
from app.utils.concurrency import get_concurrency_semaphore

async def generate_report(org, include_private):
    client = GitHubClient()
    
    # 1. Fetch Repos - calling 'get_org_repos'
    repos_data = await client.get_org_repos(org, include_private)
    
    if not isinstance(repos_data, list):
        return {
            "organization": org,
            "summary": {"total_repositories": 0, "total_users": 0, "total_access_entries": 0},
            "report": {"by_user": {}, "by_repository": {}}
        }

    sem = get_concurrency_semaphore()
    
    async def fetch_worker(repo):
        async with sem:
            repo_name = repo.get("name")
            # 2. Fetch Collaborators - calling 'get_repo_collaborators'
            cols = await client.get_repo_collaborators(org, repo_name)
            return {"repo": repo, "cols": cols if isinstance(cols, list) else []}

    # Execute all fetches concurrently
    results = await asyncio.gather(*(fetch_worker(r) for r in repos_data))
    
    by_user = {}
    by_repo = {}
    total_entries = 0

    for res in results:
        r = res["repo"]
        cols = res["cols"]
        r_name = r.get("name", "unknown")
        
        by_repo[r_name] = {
            "name": r_name, 
            "full_name": r.get("full_name", ""), 
            "private": r.get("private", False), 
            "users": [], 
            "user_count": len(cols)
        }
        
        for c in cols:
            login = c.get("login")
            if not login: continue
            
            perms = c.get("permissions", {})
            role = "read"
            if perms.get("admin"): role = "admin"
            elif perms.get("maintain"): role = "maintain"
            elif perms.get("push"): role = "write"

            by_repo[r_name]["users"].append({"login": login, "role": role})
            
            if login not in by_user:
                by_user[login] = {
                    "login": login, 
                    "avatar_url": c.get("avatar_url", ""), 
                    "profile_url": c.get("html_url", ""), 
                    "repositories": [], 
                    "repository_count": 0
                }
            
            by_user[login]["repositories"].append({"name": r_name, "role": role})
            by_user[login]["repository_count"] += 1
            total_entries += 1

    return {
        "organization": org,
        "summary": {
            "total_repositories": len(repos_data), 
            "total_users": len(by_user), 
            "total_access_entries": total_entries
        },
        "report": {"by_user": by_user, "by_repository": by_repo}
    }