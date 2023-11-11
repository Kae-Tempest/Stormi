from fastapi import WebSocket, APIRouter

router = APIRouter()
socket: list[WebSocket] = []


@router.websocket('/ws')
async def websocket(ws: WebSocket):
    await ws.accept()
    socket.append(ws)
    while True:
        data: str = await ws.receive_text()
        print('42')
        await ws.send_json(data=data)