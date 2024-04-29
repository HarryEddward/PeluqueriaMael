from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter

public_client_limiter = FastAPILimiter(
    key_func=lambda request: request.client.host,
    default_limits=["2/second"]  # Permitir 2 solicitudes por segundo por usuario
)