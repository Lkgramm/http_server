# server/http_server.py
import asyncio
import signal
import os

from server.request_handler import handle_request


class HTTPServer:
    def __init__(self, host="127.0.0.1", port=8000):
        self.host = host
        self.port = port
        self.server = None

    async def start(self):
        self.server = await asyncio.start_server(handle_request, self.host, self.port)

        addr = self.server.sockets[0].getsockname()
        print(f"Serving on {addr}")

        # Установка обработчика сигналов только на Unix-подобных системах
        if os.name != "nt":  # 'nt' — значит Windows
            loop = asyncio.get_event_loop()
            for sig in (signal.SIGINT, signal.SIGTERM):
                loop.add_signal_handler(sig, lambda: asyncio.create_task(self.stop()))

        async with self.server:
            await self.server.serve_forever()

    async def stop(self):
        print("\nShutting down server...")
        if self.server:
            self.server.close()
            await self.server.wait_closed()
        tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
        for task in tasks:
            task.cancel()
        print("All tasks cancelled.")
        asyncio.get_event_loop().stop()
