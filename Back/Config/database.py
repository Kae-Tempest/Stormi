import os

from tortoise import Tortoise


async def init():
    await Tortoise.init(
        db_url=f"postgres://{os.getenv('DBUSER')}:{os.getenv('DBPASS')}@{os.getenv('DBHOST')}:5432/{os.getenv('DB')}",
        modules={'models': ['Model.user']}
    )
    await Tortoise.generate_schemas()
