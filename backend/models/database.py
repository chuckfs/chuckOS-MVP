"""
Database models and configuration
"""

from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Text, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.sql import func
from datetime import datetime, timedelta
from typing import List
import os

# Database URL (can be configured via environment)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./jaymi_ai.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    subscription_tier = Column(String, default="free")  # free, pro, team
    files_analyzed = Column(Integer, default=0)
    searches_this_month = Column(Integer, default=0)
    created_at = Column(DateTime, default=func.now())
    last_active = Column(DateTime, default=func.now())
    
    def get_searches_remaining(self) -> int:
        """Get remaining searches for current month"""
        if self.subscription_tier == "free":
            return max(0, 100 - self.searches_this_month)
        else:
            return 999999  # Unlimited for paid plans
    
    def get_available_features(self) -> List[str]:
        """Get list of available features based on subscription"""
        base_features = ["basic_search", "file_analysis"]
        
        if self.subscription_tier in ["pro", "team"]:
            base_features.extend([
                "unlimited_search",
                "auto_organization", 
                "advanced_insights",
                "file_upload"
            ])
        
        if self.subscription_tier == "team":
            base_features.extend([
                "team_sharing",
                "admin_analytics",
                "priority_support"
            ])
        
        return base_features
    
    def can_search(self) -> bool:
        """Check if user can perform search"""
        return self.get_searches_remaining() > 0

class SearchHistory(Base):
    __tablename__ = "search_history"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    query = Column(String, nullable=False)
    results_count = Column(Integer, default=0)
    search_time = Column(Float, default=0.0)
    created_at = Column(DateTime, default=func.now())

class FilePattern(Base):
    __tablename__ = "file_patterns"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    category = Column(String, nullable=False)
    preferred_location = Column(String)
    confidence = Column(Float, default=0.0)
    learned_on = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class UserPreference(Base):
    __tablename__ = "user_preferences"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    key = Column(String, nullable=False)
    value = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class AnalyticsEvent(Base):
    __tablename__ = "analytics_events"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    event_type = Column(String, nullable=False)  # search, upload, organize, etc.
    event_data = Column(Text)  # JSON data
    created_at = Column(DateTime, default=func.now())

def create_tables():
    """Create all tables"""
    Base.metadata.create_all(bind=engine)

def get_db() -> Session:
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()