from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Howdy": "World !"}

def test_get_books():
    response = client.get("/books/1/")
    assert response.status_code == 200
    assert len(response.json()) >= 0

def test_get_books_with_filters():
    response = client.get("/books/1/?topic=c,f,d&language=en&mime_type=xml,pdf&author=Stevenson, Robert Louis&title=American")
    assert response.status_code == 200
    assert len(response.json()) >= 3

def test_get_books_with_filters_and_gutenberg_id():
    response = client.get("/books/1/?topic=c,f,d&language=en&mime_type=xml,pdf&author=Stevenson, Robert Louis&title=American&gutenberg_id=10397")
    assert response.status_code == 200
    assert len(response.json()) == 1
