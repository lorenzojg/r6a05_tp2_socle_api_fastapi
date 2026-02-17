from fastapi import FastAPI
from app.api.routers.users_router import router as users_router


app = FastAPI(title="TP FastAPI Users")
app.include_router(users_router)
