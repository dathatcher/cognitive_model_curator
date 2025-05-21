# ai_utils.py (OpenAI v1.0+ compatible)

import os
import openai
import hashlib
import json

from openai import OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

CACHE_FILE = "data/ai_cache.json"

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_cache(cache):
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=2)

def hash_prompt(prompt):
    return hashlib.sha256(prompt.encode()).hexdigest()

def run_llm_prompt(prompt: str, model="gpt-4-turbo", cache_enabled=True) -> str:
    cache = load_cache() if cache_enabled else {}
    key = hash_prompt(prompt)

    if key in cache:
        return cache[key]

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a domain-aware knowledge agent."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=500
        )
        result = response.choices[0].message.content.strip()

        if cache_enabled:
            cache[key] = result
            save_cache(cache)

        return result

    except Exception as e:
        print(f"[AI ERROR] {e}")
        return "Unclear"
