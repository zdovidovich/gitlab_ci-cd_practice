from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Book

router = APIRouter(prefix="/app", tags=["web"])
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
def show_books(request: Request, db: Session = Depends(get_db)):
    """Показывает список всех книг."""
    books = db.query(Book).order_by(Book.created_at.desc()).all()
    read_count = sum(1 for b in books if b.is_read)
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "books": books,
            "total": len(books),
            "read_count": read_count,
        },
    )


@router.post("/add", response_class=RedirectResponse)
def add_book(
    title: str = Form(...),
    author: str = Form(...),
    year: int | None = Form(None),
    db: Session = Depends(get_db),
):
    """Добавление книги через HTML-форму."""
    new_book = Book(title=title, author=author, year=year)
    db.add(new_book)
    db.commit()
    return RedirectResponse(url="/app/", status_code=303)


@router.post("/toggle/{book_id}", response_class=RedirectResponse)
def toggle_read(book_id: int, db: Session = Depends(get_db)):
    """Переключает статус 'прочитано'."""
    book = db.query(Book).filter(Book.id == book_id).first()
    if book:
        book.is_read = not book.is_read
        db.commit()
    return RedirectResponse(url="/app/", status_code=303)


@router.post("/delete/{book_id}", response_class=RedirectResponse)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """Удаление книги."""
    book = db.query(Book).filter(Book.id == book_id).first()
    if book:
        db.delete(book)
        db.commit()
    return RedirectResponse(url="/app/", status_code=303)
