import uvicorn
from fastapi import FastAPI

from core.config import settings

app = FastAPI()

if __name__ == "__main__":
    uvicorn.run(app=app, host=settings().SERVER_HOST, port=settings().SERVER_PORT)