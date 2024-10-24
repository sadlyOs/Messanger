import loguru
from fastapi import WebSocket

class ConnectManager:
    def __init__(self, websocket: WebSocket) -> None:
        self.active_connections = []
        self.websocket = websocket

    async def connect(self):
        """CONNECT EVENT"""
        await self.websocket.accept()
        loguru.logger.info(self.websocket.keys())
        self.active_connections.append(self.websocket)
        loguru.logger.info(self.active_connections)
    async def send_personal_message(self, message: str):
        """DIRECT MESSAGE"""
        await self.websocket.send_text(data=message)
        
    async def broadcast(self, message: str):
        loguru.logger.info(self.active_connections)
        for connection in self.active_connections:
            await connection.send_text(message)

    def disconnect(self):
        """disconnect event"""
        self.active_connections.remove(self.websocket)

