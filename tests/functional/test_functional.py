# tests/functional/test_functional.py

import socket


def send_http_request(method="GET", path="/"):
    """Отправляет HTTP-запрос и возвращает полный ответ от сервера"""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("127.0.0.1", 8000))
    request = f"{method} {path} HTTP/1.1\r\nHost: localhost\r\n\r\n"
    s.send(request.encode())

    # Читаем ответ полностью
    response = b""
    while True:
        part = s.recv(4096)
        if not part:
            break
        response += part

    s.close()
    return response.decode("utf-8", errors="ignore")


def extract_body(response):
    """Извлекает тело HTTP-ответа после заголовков"""
    parts = response.split("\r\n\r\n", 1)
    if len(parts) < 2:
        return ""
    return parts[1]


def test_get_index_html():
    response = send_http_request("GET", "/")
    assert "200 OK" in response, "HTTP статус должен быть 200 OK"

    body = extract_body(response)
    assert "<html>" in body, "Тело ответа должно содержать '<html>'"


def test_head_index_html():
    response = send_http_request("HEAD", "/")
    assert "200 OK" in response, "HTTP статус должен быть 200 OK"

    body = extract_body(response)
    assert body == "", "Тело ответа для HEAD-запроса должно быть пустым"


def test_404_not_found():
    response = send_http_request("GET", "/nonexistent")
    assert "404 Not Found" in response, "HTTP статус должен быть 404 Not Found"
