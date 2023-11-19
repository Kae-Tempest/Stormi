import hmac
import json
import os
from fastapi import APIRouter, Response, Request
from .websocket import manager
from enum import Enum

router = APIRouter(tags=["webhook"])

class TwitchMessage(Enum):
    TWITCH_MESSAGE_ID: str = 'Twitch-Eventsub-Message-Id'
    TWITCH_MESSAGE_TIMESTAMP: str = 'Twitch-Eventsub-Message-Timestamp'
    TWITCH_MESSAGE_SIGNATURE: str = 'Twitch-Eventsub-Message-Signature'

class TwitchMessageType(Enum):
    MESSAGE_TYPE: str = 'Twitch-Eventsub-Message-Type'
    MESSAGE_TYPE_VERIFICATION: str = 'webhook_callback_verification'
    MESSAGE_TYPE_NOTIFICATION: str = 'notification'
    MESSAGE_TYPE_REVOCATION: str = 'revocation'


@router.post('/webhook')
async def webhookService(request: Request):
    print(request.headers)
    secret = f"{os.getenv('SECRET')}"
    message = await getHmacMessage(request)
    hmac_string = 'sha256=' + getHmac(secret.encode(), message)
    if hmac.compare_digest(hmac_string, f"{request.headers.get('twitch-eventsub-message-signature')}"):
        # print("signatures match")
        notif = json.loads(await request.body())
        # print(notif)
        if request.headers.get('twitch-eventsub-message-type') == TwitchMessageType.MESSAGE_TYPE_NOTIFICATION:
            # print('Event type:' + notif.get('subscription')['type'])
            # print(json.dumps(notif.get('event'), separators=None, indent=4))
            notifType = notif.get('subscription')['type']
            eventsub = [json.dumps(notif.get('event'), separators=None, indent=4), notifType]
            for socket in manager.active_connection:
                # await socket.send_json(json.dumps(notif.get('event'), separators=None, indent=4))
                await socket.send_json(eventsub)
            Response(status_code=204)
        elif request.headers.get('twitch-eventsub-message-type') == TwitchMessageType.MESSAGE_TYPE_NOTIFICATION:
            return Response(status_code=204, content=notif.get('challenge'), headers={'Content-Type': 'text/plain'})
        elif request.headers.get('twitch-eventsub-message-type') == TwitchMessageType.MESSAGE_TYPE_REVOCATION:
            return Response(status_code=204)
        else:
            print('204')
            return Response(status_code=204)
    else:
        print('403')
        return Response(status_code=403)

async def getHmacMessage(req: Request) -> bytes:
    body = await req.body()
    return f"{req.headers.get('twitch-eventsub-message-id')}".encode() + f"{req.headers.get('twitch-eventsub-message-timestamp')}".encode() + body


def getHmac(secret: bytes, message: bytes) -> str:
    return hmac.new(secret, message, digestmod='sha256').hexdigest()
