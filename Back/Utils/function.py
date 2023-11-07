from aiohttp import ClientSession


async def fetch_url_get(url, headers):
    async with ClientSession(headers=headers) as session:
        async with session.get(url) as response:
            return await response.json()


async def fetch_url_post(url):
    async with ClientSession() as session:
        async with session.post(url) as response:
            return await response.json()
