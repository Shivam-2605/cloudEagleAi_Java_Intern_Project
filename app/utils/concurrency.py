import os
import asyncio

def get_concurrency_semaphore() -> asyncio.Semaphore:
    """
    Creates and returns an asyncio.Semaphore based on the CONCURRENCY_LIMIT env var.
    This ensures we do not overwhelm the GitHub API with too many parallel requests
    and hit their secondary rate limits.
    """
    # Default to 10 concurrent requests if not specified in .env
    limit = int(os.getenv("CONCURRENCY_LIMIT", "10"))
    return asyncio.Semaphore(limit)