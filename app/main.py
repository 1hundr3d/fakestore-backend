from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routers.auth import router as auth_router
from app.routers import products, cart
from contextlib import asynccontextmanager
import logging
import subprocess

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Сервер запускается")
    subprocess.run(["alembic", "upgrade", "head"], check=True)
    logger.info("Миграции выполнены")
    yield
    logger.info("Сервер выключается")

app = FastAPI(title='FakeStore Backend', lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router)
app.include_router(products.router)
app.include_router(cart.router)