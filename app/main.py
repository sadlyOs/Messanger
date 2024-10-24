from typing import Annotated
from fastapi import FastAPI, WebSocket, Depends, WebSocketDisconnect, HTTPException
from app.manager import ConnectManager
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

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(client_id: int, websocket: WebSocket, manager: Annotated[ConnectManager, Depends(get_manager)]):
    await manager.connect()
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"{client_id}: {data}")
    except WebSocketDisconnect:
        manager.disconnect()
        await manager.broadcast(f"{client_id}: Покинул чат")




items = {"foo": {"name": "Foo", "description": "A test item"}}

@app.get("/items/{item_id}")
async def read_item(item_id: str):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]

@app.post("/items/{item_id}")
async def create_item(item_id: str, item: dict):
    if item_id in items:
        raise HTTPException(status_code=400, detail="Item already exists")
    items[item_id] = item
    return item
