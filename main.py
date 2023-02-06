from fastapi import FastAPI
from app.routers import tests

app = FastAPI()


app.include_router(tests.router)
