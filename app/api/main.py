from fastapi import FastAPI
from app.api.routes import router
from app.health import health_check

app = FastAPI(title="Golden Goose API")

app.include_router(router)
app.add_api_route("/health", health_check, methods=["GET"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
