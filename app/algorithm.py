import time
import math
from typing import List, Dict, Any
from app.data import INITIAL_POSTS

class TrendAlgorithm:
    def __init__(self, decay_rate: float = 0.005):
        # decay_rate (lambda): higher means faster decay. 
        # 0.005 means that after 300 seconds (5 min), e^(-0.005 * 300) = e^(-1.5) = 0.22 (22% of original weight).
        self.decay_rate = decay_rate
        self.posts = {post["id"]: post.copy() for post in INITIAL_POSTS}
        self.interactions = []
        self.virtual_time_offset = 0.0  # in seconds, for simulation purposes
        
        # Populate initial interactions based on initial stats so posts start with some realistic score
        self._initialize_base_interactions()
        
    def _initialize_base_interactions(self):
        # Generate historic interaction events for each post spread over the last 6 hours (21600 seconds)
        # to justify their initial likes, views, shares.
        start_time = time.time()
        for post_id, post in self.posts.items():
            # Likes
            for i in range(post["likes"]):
                # Spread them in the past
                t = start_time - (21600 * (i + 1) / (post["likes"] + 1))
                self.interactions.append({
                    "post_id": post_id,
                    "type": "like",
                    "timestamp": t
                })
            # Views
            for i in range(post["views"]):
                t = start_time - (21600 * (i + 1) / (post["views"] + 1))
                self.interactions.append({
                    "post_id": post_id,
                    "type": "view",
                    "timestamp": t
                })
            # Shares / Saves
            for i in range(post["shares"]):
                t = start_time - (21600 * (i + 1) / (post["shares"] + 1))
                self.interactions.append({
                    "post_id": post_id,
                    "type": "share" if post["platform"] == "facebook" else "save",
                    "timestamp": t
                })

    def get_current_time(self) -> float:
        return time.time() + self.virtual_time_offset

    def advance_time(self, seconds: float):
        self.virtual_time_offset += seconds

    def reset_simulation(self):
        self.virtual_time_offset = 0.0
        self.posts = {post["id"]: post.copy() for post in INITIAL_POSTS}
        self.interactions = []
        self._initialize_base_interactions()

    def get_interaction_weight(self, interaction_type: str) -> float:
        weights = {
            "view": 1.0,
            "like": 5.0,
            "share": 10.0,
            "save": 10.0
        }
        return weights.get(interaction_type, 1.0)

    def calculate_post_score(self, post_id: str, current_time: float) -> float:
        # Sum of: weight * e^(-lambda * delta_t)
        score = 0.0
        post_interactions = [i for i in self.interactions if i["post_id"] == post_id]
        
        for item in post_interactions:
            delta_t = current_time - item["timestamp"]
            # Ignore future events if time was reset or custom timestamps are weird
            if delta_t < 0:
                continue
            
            # Exponential decay formula
            decay_factor = math.exp(-self.decay_rate * delta_t)
            weight = self.get_interaction_weight(item["type"])
            score += weight * decay_factor
            
        return round(score, 2)

    def add_interaction(self, post_id: str, interaction_type: str, custom_timestamp: float = None):
        if post_id not in self.posts:
            return False
            
        timestamp = custom_timestamp if custom_timestamp is not None else self.get_current_time()
        
        # Add interaction event
        self.interactions.append({
            "post_id": post_id,
            "type": interaction_type,
            "timestamp": timestamp
        })
        
        # Update raw counter on post dictionary
        post = self.posts[post_id]
        if interaction_type == "view":
            post["views"] += 1
        elif interaction_type == "like":
            post["likes"] += 1
        elif interaction_type in ["share", "save"]:
            post["shares"] += 1
            
        return True

    def get_posts_with_scores(self, platform: str = None) -> List[Dict[str, Any]]:
        current_time = self.get_current_time()
        result = []
        
        for post_id, post in self.posts.items():
            if platform and post["platform"] != platform:
                continue
            
            score = self.calculate_post_score(post_id, current_time)
            post_copy = post.copy()
            post_copy["current_score"] = score
            result.append(post_copy)
            
        # Sort by score descending
        result.sort(key=lambda x: x["current_score"], reverse=True)
        return result

    def get_trending_categories(self, platform: str) -> List[Dict[str, Any]]:
        posts = self.get_posts_with_scores(platform)
        category_scores = {}
        
        for p in posts:
            cat = p["category"]
            score = p["current_score"]
            category_scores[cat] = category_scores.get(cat, 0.0) + score
            
        # Format list
        result = []
        for cat, score in category_scores.items():
            result.append({
                "category": cat,
                "score": round(score, 2),
                "platform": platform
            })
            
        # Sort by score descending
        result.sort(key=lambda x: x["score"], reverse=True)
        return result
