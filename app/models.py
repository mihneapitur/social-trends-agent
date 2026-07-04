from pydantic import BaseModel
from typing import List, Optional

class InteractionRequest(BaseModel):
    post_id: str
    interaction_type: str  # "view", "like", "share", "save"
    custom_timestamp: Optional[float] = None  # to allow time simulation

class PostResponse(BaseModel):
    id: str
    platform: str
    category: str
    title: str
    description: str
    image_url: str
    tags: List[str]
    likes: int
    views: int
    shares: int
    current_score: float

class TrendCategory(BaseModel):
    category: str
    score: float
    platform: str

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    analysis: Optional[str] = None
