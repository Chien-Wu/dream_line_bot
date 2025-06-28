import redis
import json
import os

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
r = redis.Redis.from_url(REDIS_URL, decode_responses=True)

def save_user_history(user_id, history, ttl=86400):
    key = f"user_history:{user_id}"
    r.set(key, json.dumps(history), ex=ttl)

def load_user_history(user_id):
    key = f"user_history:{user_id}"
    data = r.get(key)
    if data:
        return json.loads(data)
    return []

def clear_user_history(user_id):
    key = f"user_history:{user_id}"
    r.delete(key)
