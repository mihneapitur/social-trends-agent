from pydantic import BaseModel, Field
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

class XquikPostImport(BaseModel):
    id: Optional[str] = None
    tweet_id: Optional[str] = None
    text: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    created_at: Optional[str] = None
    url: Optional[str] = None
    image_url: Optional[str] = None
    like_count: Optional[int] = None
    reply_count: Optional[int] = None
    retweet_count: Optional[int] = None
    share_count: Optional[int] = None
    view_count: Optional[int] = None
    impression_count: Optional[int] = None

class XquikImportRequest(BaseModel):
    posts: List[XquikPostImport]
