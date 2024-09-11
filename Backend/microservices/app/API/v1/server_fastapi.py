from fastapi import FastAPI, APIRouter, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi.middleware.gzip import GZipMiddleware
from fastapi_cache.backends.redis import RedisBackend
from Backend.microservices.app.API.v1.routes.admin.main import router as admin_router
from routes.client.main import router as client_router
from routes.worker.main import router as worker_router
from config.middlewares.client.restricted import RestrictedMiddleware
from Backend.microservices.app.API.v1.config.middlewares.handleError import ErrorMiddleware
import ujson
import os
import fastapi
from redis import asyncio as aioredis
from Backend.microservices.conversor.config.config import Config
from Backend.microservices.app.API.v1.logging_config import logger
from Backend.microservices.app.API.v1.db.redis_db.database import RedisClient, setup_redis_limiters_and_cache, rate_limit

# Initialize configuration and application settings
config = Config()
host = config['host']
ssl_cert = config['ssl']['cert']
ssl_key = config['ssl']['key']
app_config = config['app']
ssl = app_config['API']['ssl']
cache = app_config['API']['cache']
cors = app_config["API"]["cors"]
gzip = app_config["API"]["gzip"]
port = app_config['API']['net']['port']

# Initialize FastAPI application
app = FastAPI()

# Environment configuration: "prod" for Production or "dev" for Development
environment = "dev"

def setup_cache_and_redis():
    """
    Configures Redis for rate limiting and caching if enabled in the configuration.
    """
    if cache:
        setup_redis_limiters_and_cache(app)
        logger.info(f"API connected with Redis cache. {RedisClient.REDIS_URL}")
    else:
        logger.error(f"Failed to connect API with Redis cache. {RedisClient.REDIS_URL}")

def setup_routes():
    """
    Sets up the routes and includes specific routers for the application.
    """
    base_router = APIRouter()
    base_router.include_router(admin_router, prefix="/admin", tags=["admin"])
    base_router.include_router(client_router, prefix="/client", tags=["client"])
    base_router.include_router(worker_router, prefix="/worker", tags=["worker"])
    app.include_router(base_router, prefix="/api/app/api/v1")

def setup_middlewares():
    """
    Configures middlewares for the FastAPI application including custom middlewares,
    GZip, and CORS.
    """
    app.add_middleware(ErrorMiddleware)
    app.add_middleware(RestrictedMiddleware)

    if gzip['enabled']:
        app.add_middleware(GZipMiddleware, minimum_size=gzip['min_size'])

    if cors['enabled']:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=cors["origins"],
            allow_credentials=True,
            allow_methods=cors["methods"],
            allow_headers=cors["headers"],
        )

def setup_events():
    """
    Defines startup and shutdown events for the FastAPI application.
    """
    @app.on_event("startup")
    async def startup_event():
        pass

    @app.on_event("shutdown")
    async def shutdown_event():
        await RedisClient.disconnect()

def setup_routes_with_limiters():
    """
    Sets up routes with rate limiting.
    """
    @app.get("/error")
    @rate_limit("1/second")
    async def trigger_error(request: Request):
        """
        Triggers an error to test rate limiting.
        """
        raise ValueError("This is an Error")

    @app.get("/hidden_egg")
    @rate_limit("1/second")
    def hidden_egg(request: Request) -> HTMLResponse:
        """
        Returns an HTML response with a hidden egg image.
        """
        return HTMLResponse(
            content=f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Hidden egg</title>
                {request.client.host}
            </head>
            <body>
                <img src="https://images.pexels.com/photos/3343/easter-eggs.jpg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=0">
            </body>
            </html>
            """,
            status_code=200
        )

def run_server():
    """
    Runs the FastAPI application using Uvicorn with specified configuration.
    """
    import uvicorn

    if ssl:
        uvicorn.run(
            "server_fastapi:app",
            host=host,
            port=port,
            reload=True,
            workers=2,
            ssl_certfile=ssl_cert,
            ssl_keyfile=ssl_key,
            proxy_headers=True,
            forwarded_allow_ips="*"
        )
    else:
        uvicorn.run(
            "server_fastapi:app",
            host=host,
            port=port,
            reload=True,
            workers=2,
            proxy_headers=True,
            forwarded_allow_ips="*"
        )

# Setup application
setup_cache_and_redis()
setup_routes()
setup_middlewares()
setup_events()
setup_routes_with_limiters()

# Run the server if the script is executed directly
if __name__ == "__main__":
    run_server()

