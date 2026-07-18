from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.database import Base, engine
from app.routers.auth import router as auth_router
from app.routers import products, cart
from contextlib import asynccontextmanager
import logging
import subprocess
import os
from prometheus_fastapi_instrumentator import Instrumentator
from app.config import AppConfig

# Настраиваем логгер
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Функция жизненного цикла приложения"""
    config = AppConfig()
    config.display_config()

    logger.info("🚀 Сервер запускается...")
    
    # Выполняем миграции базы данных
    try:
        subprocess.run(["alembic", "upgrade", "head"], check=True)
        logger.info("✅ Миграции базы данных выполнены")
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Ошибка при выполнении миграций: {e}")
        raise
    
    logger.info("📡 Сервер готов принимать запросы")
    yield
    
    logger.info("🛑 Сервер выключается")

# Создаем приложение FastAPI
app = FastAPI(
    title='FakeStore Backend',
    description='Backend для интернет-магазина с аутентификацией, корзиной и кэшированием',
    version='1.0.0',
    lifespan=lifespan
)

# Добавляем метрики Prometheus
instrumentator = Instrumentator()
instrumentator.instrument(app).expose(app)

# Настраиваем CORS (Cross-Origin Resource Sharing)
# Разрешаем запросы со всех доменов (для разработки)
# В production лучше указать конкретные домены
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Можно заменить на конкретные домены, например ["http://localhost:8000"]
    allow_credentials=True,
    allow_methods=["*"],  # Разрешаем все HTTP методы (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Разрешаем все заголовки
)

# Подключаем роутеры (маршруты API)
app.include_router(auth_router)  # Маршруты аутентификации: /auth/login, /auth/register
app.include_router(products.router)  # Маршруты товаров: /products/
app.include_router(cart.router)  # Маршруты корзины: /cart/

# Находим папку frontend (находится в корне проекта)
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend")

# Маршруты для раздачи статических HTML файлов
@app.get("/index.html")
async def get_index():
    """Главная страница - каталог товаров"""
    return FileResponse(os.path.join(frontend_dir, "index.html"))

@app.get("/login.html")
async def get_login():
    """Страница входа/регистрации"""
    return FileResponse(os.path.join(frontend_dir, "login.html"))

@app.get("/cart.html")
async def get_cart():
    """Страница корзины"""
    return FileResponse(os.path.join(frontend_dir, "cart.html"))

@app.get("/admin.html")
async def get_admin():
    """Админ-панель для добавления товаров"""
    return FileResponse(os.path.join(frontend_dir, "admin.html"))

@app.get("/style.css")
async def get_css():
    """CSS стили"""
    return FileResponse(os.path.join(frontend_dir, "style.css"))

# Корневой маршрут - перенаправляет на index.html
@app.get("/")
async def root():
    """Проверка работоспособности API"""
    return {
        "message": "FakeStore API работает!",
        "frontend": "/index.html",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
async def health_check():
    """Эндпоинт для проверки здоровья приложения"""
    return {"status": "healthy"}
