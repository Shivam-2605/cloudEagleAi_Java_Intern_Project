from datetime import datetime
from pydantic import BaseModel, Field

# ==========================================
# By-User View Schemas
# ==========================================
class UserRepoAccess(BaseModel):
    name: str
    full_name: str
    role: str
    private: bool
    url: str

class UserDetail(BaseModel):
    login: str
    avatar_url: str
    profile_url: str
    repositories: list[UserRepoAccess]
    repository_count: int

# ==========================================
# By-Repository View Schemas
# ==========================================
class RepoUserAccess(BaseModel):
    login: str
    role: str

class RepoDetail(BaseModel):
    name: str
    full_name: str
    private: bool
    users: list[RepoUserAccess]
    user_count: int

# ==========================================
# Report Aggregation Schemas
# ==========================================
class ReportData(BaseModel):
    by_user: dict[str, UserDetail]
    by_repository: dict[str, RepoDetail]

class ReportSummary(BaseModel):
    total_repositories: int
    total_users: int
    total_access_entries: int

# ==========================================
# Main Response Schema
# ==========================================
class ReportResponse(BaseModel):
    organization: str
    generated_at: datetime = Field(default_factory=datetime.utcnow)
    summary: ReportSummary
    report: ReportData