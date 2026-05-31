from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .database import Base, engine
from .routers import api, web

# Создаем таблицы в БД при старте
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="BookShelf API",
    description="Простой менеджер книг. Учебный проект для DevOps практики.",
    version="1.0.0",
)

# Подключаем роутеры
app.include_router(web.router)
app.include_router(api.router)

# Статические файлы и шаблоны
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/health")
def health_check():
    """Эндпоинт для healthcheck — понадобится в Docker."""
    return {"status": "ok", "service": "bookshelf"}


@app.get("/")
def root():
    """Приветствие API. Главная страница — на /app."""
    return {
        "message": "Добро пожаловать в BookShelf API!",
        "docs": "/docs",
        "web": "/app",
    }
