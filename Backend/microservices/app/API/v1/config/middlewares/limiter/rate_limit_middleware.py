from fastapi import Request, FastAPI
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from fastapi.responses import JSONResponse

# Configuración del Limiter
limiter = Limiter(key_func=get_remote_address)

# Manejador de excepciones para RateLimitExceeded
async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"message": "Has excedido el límite de solicitudes. Por favor, inténtalo más tarde."}
    )

def add_rate_limit_middleware(app: FastAPI):
    app.state.limiter = limiter
    app.add_middleware(SlowAPIMiddleware)
    
    # Asignar el manejador de excepciones para RateLimitExceeded
    app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)

    # Middleware para aplicar el limitador global
    @app.middleware("http")
    async def global_rate_limiter(request: Request, call_next):
        response = await limiter.limit("1/2 seconds")(call_next)(request)
        return response
