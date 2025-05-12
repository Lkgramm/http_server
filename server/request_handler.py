# server/request_handler.py

import os
import mimetypes
import asyncio


async def handle_request(reader, writer):
    try:
        # Читаем запрос клиента
        data = await reader.read(65535)
        if not data:
            writer.close()
            return

        # Декодируем и разбираем первую строку запроса
        request_line = data.decode("utf-8").split("\r\n")[0]
        if not request_line:
            writer.close()
            return

        method, path, _ = request_line.split(" ", 2)

        # Логируем запрос
        addr = writer.get_extra_info("peername")
        print(f"Received {method} request from {addr} for {path}")

        # Проверяем поддерживаемые методы
        if method not in ("GET", "HEAD"):
            response = "HTTP/1.1 405 Method Not Allowed\r\n\r\n"
            writer.write(response.encode())
            await writer.drain()
            writer.close()
            return

        # Формируем путь к файлу
        file_path = get_file_path(path)
        if not os.path.exists(file_path) or not os.path.isfile(file_path):
            response = "HTTP/1.1 404 Not Found\r\n\r\n"
            writer.write(response.encode())
            await writer.drain()
            writer.close()
            return

        # Определяем MIME-тип
        content_type, _ = mimetypes.guess_type(file_path)
        content_type = content_type or "application/octet-stream"

        # Асинхронное чтение файла через поток
        try:
            loop = asyncio.get_event_loop()
            body = await loop.run_in_executor(None, read_file_sync, file_path)

            # Формируем заголовки
            header = (
                f"HTTP/1.1 200 OK\r\n"
                f"Content-Type: {content_type}\r\n"
                f"Content-Length: {len(body)}\r\n"
                f"\r\n"
            )

            writer.write(header.encode())

            # GET — отправляем тело, HEAD — только заголовки
            if method == "GET":
                writer.write(body)

            await writer.drain()

        except Exception as e:
            print(f"[ERROR] Reading file {file_path}: {e}")
            response = "HTTP/1.1 500 Internal Server Error\r\n\r\n"
            writer.write(response.encode())
            await writer.drain()

        finally:
            writer.close()
            await writer.wait_closed()

    except asyncio.CancelledError:
        print("Request handler cancelled")
    except Exception as e:
        print(f"[ERROR] Handling client: {e}")
        writer.close()


def get_file_path(requested_path: str) -> str:
    """Преобразует URL-путь в путь к файлу в www"""
    if requested_path == "/":
        requested_path = "/index.html"
    return os.path.join("www", requested_path.lstrip("/"))


def read_file_sync(file_path: str) -> bytes:
    """Синхронное чтение файла (выполняется в пуле потоков)"""
    with open(file_path, "rb") as f:
        return f.read()
