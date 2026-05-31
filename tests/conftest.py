import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app

# Используем in-memory SQLite для тестов
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_bookshelf.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Переопределяем зависимость БД для тестов."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function")
def db_session():
    """Создает таблицы перед тестом и удаляет после."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """HTTP-клиент для тестирования API."""
    return TestClient(app)


@pytest.fixture
def sample_book(db_session):
    """Создает тестовую книгу в БД."""
    from app.models import Book
    
    book = Book(
        title="1984",
        author="George Orwell",
        year=1949,
        is_read=False,
    )
    db_session.add(book)
    db_session.commit()
    db_session.refresh(book)
    return book