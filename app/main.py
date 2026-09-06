from fastapi import FastAPI
from app.api.routes import router
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

app = FastAPI()

app.include_router(router)

@app.get("/")
def root():
    return {"Message": "ASYNC URL METADATA API PROJECT IS RUNNING"}