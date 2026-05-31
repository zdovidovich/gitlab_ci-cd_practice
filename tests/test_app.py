def test_health_check(client):
    """Проверяем healthcheck эндпоинт."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "bookshelf"


def test_root_endpoint(client):
    """Проверяем корневой эндпоинт."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data


def test_create_book_api(client):
    """Создание книги через API."""
    book_data = {
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "year": 1925,
        "is_read": False,
    }
    response = client.post("/api/books/", json=book_data)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "The Great Gatsby"
    assert data["author"] == "F. Scott Fitzgerald"
    assert "id" in data


def test_list_books_api(client, sample_book):
    """Получение списка книг через API."""
    response = client.get("/api/books/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert any(book["title"] == "1984" for book in data)


def test_get_book_api(client, sample_book):
    """Получение конкретной книги по ID."""
    response = client.get(f"/api/books/{sample_book.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "1984"


def test_get_nonexistent_book_api(client):
    """Попытка получить несуществующую книгу."""
    response = client.get("/api/books/99999")
    assert response.status_code == 404


def test_update_book_api(client, sample_book):
    """Обновление книги через API."""
    update_data = {"is_read": True}
    response = client.patch(f"/api/books/{sample_book.id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["is_read"] is True


def test_delete_book_api(client, sample_book):
    """Удаление книги через API."""
    response = client.delete(f"/api/books/{sample_book.id}")
    assert response.status_code == 204
    
    # Проверяем, что книга действительно удалена
    response = client.get(f"/api/books/{sample_book.id}")
    assert response.status_code == 404


def test_web_index_page(client):
    """Проверяем загрузку главной страницы веб-интерфейса."""
    response = client.get("/app/")
    assert response.status_code == 200
    assert "BookShelf" in response.text


def test_web_add_book(client):
    """Добавление книги через веб-форму."""
    form_data = {
        "title": "To Kill a Mockingbird",
        "author": "Harper Lee",
        "year": "1960",
    }
    response = client.post("/app/add", data=form_data, follow_redirects=False)
    assert response.status_code == 303
    assert response.headers["location"] == "/app/"


def test_web_toggle_book(client, sample_book):
    """Переключение статуса прочитано через веб-интерфейс."""
    response = client.post(f"/app/toggle/{sample_book.id}", follow_redirects=False)
    assert response.status_code == 303


def test_web_delete_book(client, sample_book):
    """Удаление книги через веб-интерфейс."""
    response = client.post(f"/app/delete/{sample_book.id}", follow_redirects=False)
    assert response.status_code == 303