from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine
from app.models import medicine, pet
from app.routers import medicine as medicine_router, pet as pet_router, schedule as schedule_router

medicine.Base.metadata.create_all(bind=engine)
pet.Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルーター登録
app.include_router(medicine_router.router)
app.include_router(pet_router.router)
app.include_router(schedule_router.router)

@app.get("/")
def root():
    return {"message": "Hello from FastAPI"}
