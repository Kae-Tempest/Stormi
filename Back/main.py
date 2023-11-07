from aiohttp import web
from dotenv import load_dotenv
from tortoise import run_async
from Config.database import init
from Controler.twitchControler import get_token, get_user
from Services.webhook import webhookService
load_dotenv()

run_async(init())
app = web.Application()
app.add_routes([
    web.get('/get_token', get_token),
    web.get('/users/{username}', get_user),
    web.post('/eventsub', webhookService)
])

web.run_app(app)

"""https://id.twitch.tv/oauth2/authorize?response_type=code
&client_id=1arx03yfjupkiq3ryipmx06epw05m4
&redirect_uri=http://localhost:8080/get_token
&scope=channel%3Aread%3Ahype_train%20channel%3Aread%3Asubscriptions%20moderator%3Aread%3Afollowers%20chat%3Aread"""
