import time

from cachetools import TTLCache
from fastapi import FastAPI, Path
from nonebot import get_driver, get_app
from nonebot.adapters.onebot.v11 import Bot
from starlette.responses import Response

files = TTLCache(maxsize=2 ** 31 - 1, ttl=300)

app: FastAPI = get_app()


@app.get("/file_center/{file_id}")
async def get_file(file_id: int = Path()):
    data = files.get(file_id, None)
    if data is None:
        return Response(status_code=404)
    return Response(data)


async def send_group_file(bot: Bot, group_id: int, filename: str, data: bytes):
    file_id = time.time_ns()
    files[file_id] = data

    driver = get_driver()

    download_result = await bot.download_file(
        url=f"http://{driver.config.host}:{driver.config.port}/file_center/{file_id}",
        thread_count=1
    )

    await bot.upload_group_file(group_id=group_id,
                                file=download_result["file"],
                                name=filename)


async def send_private_file(bot: Bot, user_id: int, filename: str, data: bytes):
    file_id = time.time_ns()
    files[file_id] = data

    driver = get_driver()

    download_result = await bot.download_file(
        url=f"http://{driver.config.host}:{driver.config.port}/file_center/{file_id}",
        thread_count=1
    )

    await bot.upload_private_file(user_id=user_id,
                                  file=download_result["file"],
                                  name=filename)
