from fastapi import FastAPI
from typing import Dict
import time
from random import random, randint
from time import perf_counter
import concurrent.futures as cf
import multiprocessing as mp

from .profiling import profiling_queue

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


@app.post("/mp")
async def mp_endpoint() -> Dict[str, str]:
    i = randint(0, 1_000_000)
    profiling_queue.put(i)
    return {"status": "async"}
