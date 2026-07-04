from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from app.models import ChatRequest, ChatResponse, InteractionRequest, XquikImportRequest
from app.algorithm import TrendAlgorithm
from app.agent import AIAgent
from app.data import MY_PROFILES_STATS

app = FastAPI(title="Social Trends AI Agent API")

# Enable CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instantiate algorithm and agent
algo = TrendAlgorithm(decay_rate=0.005)
agent = AIAgent(algo)
SUPPORTED_PLATFORMS = ["facebook", "pinterest", "xquik"]

def require_supported_platform(platform: str) -> None:
    if platform not in SUPPORTED_PLATFORMS:
        valid_platforms = "', '".join(SUPPORTED_PLATFORMS)
        raise HTTPException(status_code=400, detail=f"Invalid platform. Must be '{valid_platforms}'.")

def dump_model(model):
    if hasattr(model, "model_dump"):
        return model.model_dump(exclude_none=True)
    return model.dict(exclude_none=True)

@app.get("/api/feed")
def get_feed(platform: str = None):
    if platform:
        require_supported_platform(platform)
    try:
        posts = algo.get_posts_with_scores(platform)
        return posts
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/interact")
def record_interaction(req: InteractionRequest):
    success = algo.add_interaction(
        post_id=req.post_id,
        interaction_type=req.interaction_type,
        custom_timestamp=req.custom_timestamp
    )
    if not success:
        raise HTTPException(status_code=404, detail="Post not found.")
    
    # Return updated post details
    current_time = algo.get_current_time()
    post = algo.posts[req.post_id]
    score = algo.calculate_post_score(req.post_id, current_time)
    
    post_copy = post.copy()
    post_copy["current_score"] = score
    return post_copy

@app.get("/api/trends")
def get_trends(platform: str):
    require_supported_platform(platform)
    return algo.get_trending_categories(platform)

@app.post("/api/import/xquik")
def import_xquik_posts(req: XquikImportRequest):
    rows = [dump_model(post) for post in req.posts]
    imported_posts = algo.import_xquik_posts(rows)
    return {
        "imported": len(imported_posts),
        "platform": "xquik",
        "posts": imported_posts,
    }

@app.get("/api/my-profiles")
def get_my_profiles():
    return MY_PROFILES_STATS

@app.post("/api/chat", response_model=ChatResponse)
def chat_with_agent(req: ChatRequest):
    try:
        response_text, analysis_text = agent.respond_to_user(req.message)
        return ChatResponse(response=response_text, analysis=analysis_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/simulate/advance")
def advance_time(seconds: float):
    if seconds <= 0:
        raise HTTPException(status_code=400, detail="Seconds must be positive.")
    algo.advance_time(seconds)
    return {
        "message": f"Simulated time advanced by {seconds} seconds ({round(seconds/60, 2)} minutes).",
        "current_time": algo.get_current_time(),
        "virtual_offset": algo.virtual_time_offset
    }

@app.post("/api/simulate/reset")
def reset_simulation():
    algo.reset_simulation()
    agent.clear_chat_history()
    return {
        "message": "Simulation reset successfully.",
        "current_time": algo.get_current_time(),
        "virtual_offset": algo.virtual_time_offset
    }

@app.get("/api/simulate/time")
def get_simulated_time():
    return {
        "current_time": algo.get_current_time(),
        "virtual_offset": algo.virtual_time_offset
    }

# Serve static files
# Note: Root endpoint is defined before mounting static files to avoid conflicts.
@app.get("/")
def read_root():
    static_file_path = os.path.join("static", "index.html")
    if not os.path.exists(static_file_path):
        # Fallback if static folder isn't populated yet
        return {"message": "Social Media Trends Agent API running. Static files are not yet created."}
    return FileResponse(static_file_path)

# Mount the static directory for CSS, JS, assets
app.mount("/", StaticFiles(directory="static"), name="static")
