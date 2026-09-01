from fastapi import FastAPI
from routers import users,recipes,cart
from database import Base, engine
import models
from fastapi.middleware.cors import CORSMiddleware




app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5501",
        "http://localhost:5501"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
Base.metadata.create_all(bind=engine)
app.include_router(users.router)
app.include_router(recipes.router)
app.include_router(cart.router)