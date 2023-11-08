import hmac
import json
import os
from fastapi import APIRouter, Response

router = APIRouter()


TWITCH_MESSAGE_ID = 'Twitch.py-Eventsub-Message-Id'
TWITCH_MESSAGE_TIMESTAMP = 'Twitch.py-Eventsub-Message-Timestamp'
TWITCH_MESSAGE_SIGNATURE = 'Twitch.py-Eventsub-Message-Signature'
MESSAGE_TYPE = 'Twitch.py-Eventsub-Message-Type'

MESSAGE_TYPE_VERIFICATION = 'webhook_callback_verification'
MESSAGE_TYPE_NOTIFICATION = 'notification'
MESSAGE_TYPE_REVOCATION = 'revocation'

@router.post('/post')
async def webhookService(request):
    secret = os.getenv('SECRET')
    message = await getHmacMessage(request)
    hmac_string = 'sha256=' + getHmac(secret, message)
    if hmac.compare_digest(hmac_string, request.headers[TWITCH_MESSAGE_SIGNATURE]):
        print("signatures match")
        notif = json.loads(await request.text())
        print(notif)
        if MESSAGE_TYPE_NOTIFICATION == request.headers[MESSAGE_TYPE]:
            print('Event type:' + notif.get('subscription')['type'])
            print(json.dumps(notif.get('event'), separators=None, indent=4))
            Response(status_code=204)
        elif MESSAGE_TYPE_VERIFICATION == request.headers[MESSAGE_TYPE]:
            return Response(status_code=204, content=notif.get('challenge'), headers={'Content-Type': 'text/plain'})
        elif MESSAGE_TYPE_REVOCATION == request.headers[MESSAGE_TYPE]:
            Response(status_code=204)
        else:
            print('204')
            Response(status_code=204)
    else:
        print('403')
        Response(status_code=403)


async def getHmacMessage(req):
    body = await req.text()
    return req.headers[TWITCH_MESSAGE_ID].encode() + req.headers[TWITCH_MESSAGE_TIMESTAMP].encode() + body.encode()


def getHmac(secret: str, message: str) -> str:
    return hmac.new(secret.encode(), message, digestmod='sha256').hexdigest()
