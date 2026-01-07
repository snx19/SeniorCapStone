"""Main FastAPI application."""
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from jinja2 import Environment, FileSystemLoader
from app.api.router import api_router
from app.db.base import Base, engine
from app.logging_config import setup_logging

# Setup logging
setup_logging()

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="AI Oral Exam Grader",
    description="AI-powered oral exam grading system",
    version="0.1.0"
)

# Include API routes
app.include_router(api_router, prefix="/api")

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Templates
env = Environment(loader=FileSystemLoader("app/templates"))


def render_template(template_name: str, context: dict) -> HTMLResponse:
    """Render a Jinja2 template."""
    template = env.get_template(template_name)
    html_content = template.render(**context)
    return HTMLResponse(content=html_content)


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Root page - login form."""
    error = request.query_params.get("error", "")
    return render_template("login.html", {"request": request, "error": error})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

