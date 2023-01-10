from fastapi import FastAPI
import typing
import asyncio
from typing import Dict
from random import random, randint
from time import perf_counter
import concurrent.futures as cf
import multiprocessing as mp
from fastapi import FastAPI, Request

from .profiling import pipe_send, queue

app = FastAPI()


def profile() -> int:
    i = 0
    start = perf_counter()

    while (perf_counter() - start) < 1:
        i = i + randint(0, 1_000_000)

    return i


future_pool = cf.ProcessPoolExecutor(max_workers=10)


@app.post("/future")
async def root() -> Dict[str, str]:
    future = future_pool.submit(profile)
    return {"message": "Hello World", "result": str(future.result())}


@app.post("/queue")
async def test_queue(request: Request) -> None:
    csv: bytes = await request.body()
    print(f"[CONTROLLER] Sending bytes over to profiling process {str(type(csv))}")
    queue.put(csv)


async def async_send(conn: typing.Any, payload: typing.Any) -> None:
    conn.send(payload)


@app.post("/pipe")
async def test_pipe(request: Request) -> None:
    csv: bytes = await request.body()
    print(f"[CONTROLLER] Sending bytes over to profiling process {str(type(csv))}")
    pipe_send.send(csv)
    # asyncio.get_running_loop().create_task(async_send(pipe[0], csv))
