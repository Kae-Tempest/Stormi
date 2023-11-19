from fastapi import WebSocket, APIRouter, WebSocketDisconnect

router = APIRouter()


class ConnectionManager:
    def __init__(self):
        self.active_connection: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connection.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connection.remove(websocket)
        
    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_json(message)


manager = ConnectionManager()


@router.websocket('/ws')
async def websocket(ws: WebSocket):
    await manager.connect(ws)
    try:
        while True:
            data: str = await ws.receive_text()
            await manager.send_personal_message(data, ws)
    except WebSocketDisconnect:
        manager.disconnect(ws)
