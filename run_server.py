import asyncio
from server.http_server import HTTPServer


async def main():
    server = HTTPServer(port=8000)
    await server.start()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Server stopped manually.")