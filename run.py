"""Simple script to run the application."""
import uvicorn

from app.settings import get_settings
get_settings.cache_clear()
settings = get_settings()

print("LLM_MODEL =", settings.llm_model)
print("TOGETHER_API_KEY =", settings.together_api_key[:5] + "…")

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

