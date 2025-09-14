"""
Pydantic schemas for API request/response models
"""

from pydantic import BaseModel, EmailStr
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class SubscriptionTier(str, Enum):
    FREE = "free"
    PRO = "pro"
    TEAM = "team"

# Request models
class FileSearchRequest(BaseModel):
    query: str
    file_paths: Optional[List[str]] = None
    max_results: Optional[int] = 20

class UserRegistrationRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None

class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str

# Response models
class FileSearchResult(BaseModel):
    filename: str
    path: str
    full_path: str
    size: int
    size_mb: float
    modified: str
    category: str
    relevance_score: float

class FileSearchResponse(BaseModel):
    query: str
    results: List[FileSearchResult]
    total_found: int
    search_time: float

class FileAnalysisResponse(BaseModel):
    total_files: int
    total_size: int
    total_size_mb: float
    categories: Dict[str, int]
    category_sizes: Dict[str, float]
    suggestions: List[Dict[str, Any]]
    analyzed_at: str

class UserResponse(BaseModel):
    id: int
    email: str
    subscription_tier: SubscriptionTier
    files_analyzed: int
    searches_this_month: int
    created_at: datetime

class SubscriptionResponse(BaseModel):
    tier: SubscriptionTier
    searches_remaining: int
    features_available: List[str]
    next_billing_date: Optional[datetime] = None

class InsightResponse(BaseModel):
    type: str
    title: str
    message: str
    priority: str

class AnalyticsResponse(BaseModel):
    total_users: int
    active_users: int
    total_searches: int
    popular_queries: List[Dict[str, Any]]
    subscription_distribution: Dict[str, int]

# Database models
class Token(BaseModel):
    access_token: str
    token_type: str