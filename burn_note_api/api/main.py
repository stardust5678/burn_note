from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.db import create_db_and_tables

from .routes import router as api_router

app = FastAPI()

# TODO
# origins = [
#     "http://localhost",
#     "http://localhost:5173",
# ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

@app.on_event("startup")
async def on_startup():
    create_db_and_tables()
