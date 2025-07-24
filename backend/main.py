#!/usr/bin/env python3
"""
Jaymi AI File Assistant - SaaS Backend
FastAPI application for file intelligence web service
"""

from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List, Optional
import json
import os
from pathlib import Path
from datetime import datetime
import tempfile
import shutil

# Import the core file intelligence (extract from existing code)
from backend.core.file_intelligence import JaymiFileIntelligenceAPI
from backend.core.auth import get_current_user, create_access_token, create_user, authenticate_user
from backend.models.database import get_db, User, create_tables
from backend.models.schemas import (
    FileSearchRequest, FileSearchResponse,
    FileAnalysisResponse, UserResponse,
    SubscriptionResponse, UserRegistrationRequest, 
    UserLoginRequest, Token
)

app = FastAPI(
    title="Jaymi AI File Assistant",
    description="Smart file search, analysis, and organization powered by AI",
    version="1.0.0"
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://jaymi-ai.com"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Initialize database and file intelligence engine
create_tables()
file_intelligence = JaymiFileIntelligenceAPI()

@app.get("/")
async def root():
    """Welcome message"""
    return {
        "message": "Welcome to Jaymi AI File Assistant API",
        "version": "1.0.0",
        "features": [
            "Smart file search with natural language",
            "AI-powered file organization",
            "File system analysis and insights",
            "Learning and memory system"
        ]
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# Authentication endpoints
@app.post("/auth/register")
async def register(request: UserRegistrationRequest, db = Depends(get_db)):
    """Register new user"""
    try:
        user = create_user(db, request.email, request.password, request.full_name)
        access_token = create_access_token(data={"sub": user.email})
        return {"access_token": access_token, "token_type": "bearer", "user": UserResponse(
            id=user.id,
            email=user.email,
            subscription_tier=user.subscription_tier,
            files_analyzed=user.files_analyzed,
            searches_this_month=user.searches_this_month,
            created_at=user.created_at
        )}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/auth/login")
async def login(request: UserLoginRequest, db = Depends(get_db)):
    """User login"""
    user = authenticate_user(db, request.email, request.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password"
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer", "user": UserResponse(
        id=user.id,
        email=user.email,
        subscription_tier=user.subscription_tier,
        files_analyzed=user.files_analyzed,
        searches_this_month=user.searches_this_month,
        created_at=user.created_at
    )}

# File intelligence endpoints
@app.post("/files/search", response_model=FileSearchResponse)
async def search_files(
    request: FileSearchRequest,
    current_user = Depends(get_current_user),
    db = Depends(get_db)
):
    """Smart file search with natural language"""
    try:
        # Use the extracted file intelligence
        results = await file_intelligence.smart_search(
            query=request.query,
            user_id=current_user.id,
            file_paths=request.file_paths or []
        )
        
        return FileSearchResponse(
            query=request.query,
            results=results,
            total_found=len(results),
            search_time=results.get('search_time', 0)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/files/upload")
async def upload_files(
    files: List[UploadFile] = File(...),
    current_user = Depends(get_current_user),
    db = Depends(get_db)
):
    """Upload files for analysis"""
    try:
        uploaded_files = []
        
        for file in files:
            # Create temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=file.filename) as temp_file:
                shutil.copyfileobj(file.file, temp_file)
                temp_path = temp_file.name
            
            # Analyze the uploaded file
            analysis = await file_intelligence.analyze_file(
                file_path=temp_path,
                original_name=file.filename,
                user_id=current_user.id
            )
            
            uploaded_files.append({
                "filename": file.filename,
                "size": file.size,
                "analysis": analysis
            })
            
            # Clean up temp file
            os.unlink(temp_path)
        
        return {
            "message": f"Successfully analyzed {len(uploaded_files)} files",
            "files": uploaded_files
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/files/analyze", response_model=FileAnalysisResponse)
async def analyze_file_system(
    path: Optional[str] = None,
    current_user = Depends(get_current_user),
    db = Depends(get_db)
):
    """Analyze file system and generate insights"""
    try:
        # Use default paths if none provided
        if not path:
            analysis = await file_intelligence.analyze_system(
                user_id=current_user.id
            )
        else:
            analysis = await file_intelligence.analyze_path(
                path=path,
                user_id=current_user.id
            )
        
        return FileAnalysisResponse(**analysis)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/files/insights")
async def get_file_insights(
    current_user = Depends(get_current_user),
    db = Depends(get_db)
):
    """Get AI-generated file system insights"""
    try:
        insights = await file_intelligence.get_insights(
            user_id=current_user.id
        )
        
        return {
            "insights": insights,
            "generated_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/files/organize")
async def auto_organize_files(
    path: Optional[str] = None,
    dry_run: bool = True,
    current_user = Depends(get_current_user),
    db = Depends(get_db)
):
    """Auto-organize files based on learned patterns"""
    try:
        results = await file_intelligence.auto_organize(
            path=path,
            user_id=current_user.id,
            dry_run=dry_run
        )
        
        return {
            "action": "dry_run" if dry_run else "organized",
            "results": results
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# User management endpoints
@app.get("/user/profile", response_model=UserResponse)
async def get_user_profile(current_user = Depends(get_current_user)):
    """Get current user profile"""
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        subscription_tier=current_user.subscription_tier,
        files_analyzed=current_user.files_analyzed,
        searches_this_month=current_user.searches_this_month
    )

@app.get("/user/subscription", response_model=SubscriptionResponse)
async def get_subscription_info(current_user = Depends(get_current_user)):
    """Get user subscription information"""
    return SubscriptionResponse(
        tier=current_user.subscription_tier,
        searches_remaining=current_user.get_searches_remaining(),
        features_available=current_user.get_available_features()
    )

# Analytics endpoints (for business intelligence)
@app.get("/admin/analytics")
async def get_analytics(current_user = Depends(get_current_user)):
    """Get usage analytics (admin only)"""
    # Admin-only endpoint for business metrics
    pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)