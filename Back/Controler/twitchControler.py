import os
from urllib.parse import urlencode
from Utils.function import fetch_url_post, fetch_url_get
from aiohttp import web
from Model.user import User, UserSchema


async def get_token(request):
    token = request.query['code']
    scope = request.query['scope']
    client = os.getenv('CLIENT')
    secret = os.getenv('SECRET')
    params = {
        "client_id": client,
        "client_secret": secret,
        "code": token,
        "grant_type": "authorization_code",
        "redirect_uri": "http://localhost:8080"
    }
    url = f"https://id.twitch.tv/oauth2/token?{urlencode(params)}"
    oauth = await fetch_url_post(url)
    headers = {
        "Authorization": "Bearer " + oauth['access_token'],
        "Client-Id": client
    }
    userdata = await fetch_url_get("https://api.twitch.tv/helix/users", headers)
    userdata = userdata.get("data", [{}])[0]
    if not userdata:
        print('No data returned')
    else:
        avatar = userdata.get('profile_image_url')
        name = userdata.get('login')
        user_id = userdata.get('id')
        email = userdata.get('email')
        user = User(
            id=user_id,
            name=name,
            email=email,
            access=oauth['access_token'],
            avatar=avatar
        )
        existing_user = await UserSchema.from_tortoise_orm(await User.filter(name=name).first())
        if existing_user:
            print('connect to dashboard')
        else:
            await user.save()
            print('connect to dashboard')
        return web.HTTPFound(location=f"/users/{name}")


async def get_user(request):
    username = request.match_info.get('username')
    user = await UserSchema.from_tortoise_orm(await User.filter(name=username).first())
    return web.Response(text=f"{user}")
