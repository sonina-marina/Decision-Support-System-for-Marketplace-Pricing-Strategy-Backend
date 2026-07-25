from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.exceptions.registration import register_exception_handlers
from src.api.router import router

app = FastAPI()

register_exception_handlers(app)

app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)
