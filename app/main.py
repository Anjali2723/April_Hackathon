from fastapi import FastAPI
from app.database import Base, engine
from app.routers.users import router as users_router
from app.routers.orders import router as orders_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(users_router)
app.include_router(orders_router)

@app.get("/")
def root():
    return {"message": "API running"}

