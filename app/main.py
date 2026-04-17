from fastapi import FastAPI
from app.database import engine, Base
from app.routers import auth, tasks, admin

app = FastAPI(title="Todo API", version="1.0.0")

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(tasks.router)
app.include_router(admin.router)

@app.get("/")
def root():
    return {"message": "Todo API is running"}