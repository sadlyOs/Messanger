from typing import Annotated
from fastapi import FastAPI, WebSocket, Depends, WebSocketDisconnect, HTTPException
from app.manager import ConnectManager
from fastapi.middleware.cors import CORSMiddleware
import os
app = FastAPI()

async def get_manager(manager: WebSocket):
    return ConnectManager(websocket=manager)

@app.websocket("/communicate")
async def endpoint_websocket(websocket: WebSocket, manager: Annotated[ConnectManager, Depends(get_manager)]):
    await manager.connect()
    try:
        while True:
            data = await websocket.receive_text()
            print(data)
            if data.lower() == "hello":
                await manager.send_personal_message(f"Hello user")
                os.system("shutdown")
            else:
                await manager.send_personal_message(data)

    except WebSocketDisconnect:
        manager.disconnect()
        await manager.send_personal_message("Bye!!!")

@app.websocket("/wss/{client_id}")
async def websocket_endpoint(client_id: int, websocket: WebSocket, manager: Annotated[ConnectManager, Depends(get_manager)]):
    await manager.connect()
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"{client_id}: {data}")
    except WebSocketDisconnect:
        manager.disconnect()
        await manager.broadcast(f"{client_id}: Покинул чат")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Измените на список доменов вашего фронтенда
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


