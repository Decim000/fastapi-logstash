import uuid
import logging
import aiohttp

from fastapi import FastAPI, Request
from functools import wraps
from starlette.datastructures import MutableHeaders

from logger import Logger

app = FastAPI()
logger = Logger('Logger for slave')


def logs(func):
    @wraps(func)
    async def wrap_func(request: Request, *args, **kwargs):
        request_uuid = str(uuid.uuid4())
        if not request.headers.get("X-UUID-Header"):
            # logging.info(f'Set UUID-Header for slave service | UUID: {request_uuid}')
            # print(f'Set UUID-Header for slave service | UUID: {request_uuid}')
            await logger.info_on_send_request(message='Init from slave', uuid=request_uuid)
            
            # setting custom headers
            new_header = MutableHeaders(request._headers)
            new_header["X-UUID-Header"]=request_uuid
            request._headers = new_header
            request.scope.update(headers=request.headers.raw)

        else:
            await logger.info_on_get_request(message='Got request from master', uuid=request.headers.get("X-UUID-Header"))
            # logging.info(f'Got request for slave service | UUID: {request.headers.get("X-UUID-Header")}')
            # print(f'Got request for slave service | UUID: {request.headers.get("X-UUID-Header")}')

        return await func(request, *args, **kwargs)

    return wrap_func

# получает запрос от мастера
@app.get("/slave")
@logs
async def root(request: Request):
    return {"message from slave": request.headers.get("X-UUID-Header")}

# отправляет запрос мастеру
@app.get("/slave-sending")
@logs
async def send(request: Request):

    async with aiohttp.ClientSession() as session:
        headers = {'X-UUID-Header': request.headers.get("X-UUID-Header")}

        # async with session.get(url='http://service-master:8000/master-receiving', headers=headers) as response:
        #     print("Status:", response.status)
        #     print("Status:", await response.text())
        async with session.get(url='http://service-master/master-receiving', headers=headers) as response:
            print("Status:", response.status)
            print("Status:", await response.text())

    return {"message": request.headers.get("X-UUID-Header")}