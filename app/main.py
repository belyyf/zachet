from fastapi import FastAPI
from app.database import engine, Base
from app.routers import auth, tasks, admin

app = FastAPI(title="Todo API", version="1.0.0")

@app.on_event("startup")
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(auth.router)
app.include_router(tasks.router)
app.include_router(admin.router)

@app.get("/")
async def root():
    return {"message": "Todo API is running"}