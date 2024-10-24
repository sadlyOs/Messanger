import loguru
from fastapi import WebSocket

class ConnectManager:
    def __init__(self) -> None:
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        """CONNECT EVENT"""
        await self.websocket.accept()
        loguru.logger.info(websocket.keys())
        self.active_connections.append(websocket)
        loguru.logger.info(self.active_connections)
    async def send_personal_message(self, message: str):
        """DIRECT MESSAGE"""
        await websocket.send_text(data=message)
        
    async def broadcast(self, message: str):
        loguru.logger.info(self.active_connections)
        for connection in self.active_connections:
            await connection.send_text(message)

    def disconnect(self, websocket: WebSocket):
        """disconnect event"""
        self.active_connections.remove(websocket)

