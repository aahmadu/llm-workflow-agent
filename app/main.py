from fastapi import FastAPI
from app.routes import sales

app = FastAPI()
app.include_router(sales.router)