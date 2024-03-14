from fastapi.middleware.cors import CORSMiddleware

allow = {
    "origins": [
        "http://localhost:5173"
        #'http://localhost:9712'
    ],
    "methods": [
        "*"
    ],
    "headers": [
        "*"
    ],
}
