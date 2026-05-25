"""
Pydantic schemas for API request/response validation.
"""

from app.models.common import PaginationParams, PaginatedResponse
from app.models.insight import InsightCreate, InsightResponse, InsightFilter
from app.models.event import EventCreate, EventResponse, EventFilter
from app.models.scoring import ScoringRequest, ScoringResponse
from app.models.prediction import PredictionRequest, PredictionResponse
from app.models.user import UserCreate, UserResponse, UserLogin, Token

__all__ = [
    # Common
    "PaginationParams",
    "PaginatedResponse",
    # Insights
    "InsightCreate",
    "InsightResponse",
    "InsightFilter",
    # Events
    "EventCreate",
    "EventResponse",
    "EventFilter",
    # Scoring
    "ScoringRequest",
    "ScoringResponse",
    # Prediction
    "PredictionRequest",
    "PredictionResponse",
    # User
    "UserCreate",
    "UserResponse",
    "UserLogin",
    "Token",
]