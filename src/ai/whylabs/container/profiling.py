import concurrent.futures as cf
import typing
from time import perf_counter
import multiprocessing as mp
from multiprocessing.connection import Connection
from time import perf_counter
from random import randint
from whylogs.core import DatasetProfile
import pandas as pd
import io


queue: mp.Queue = mp.Queue(100)
pipe_rcv, pipe_send = mp.Pipe(False)


def _fake_work() -> int:
    i = 0
    start = perf_counter()

    # simulate some profiling
    while (perf_counter() - start) < 0.02:
        i = i + randint(0, 1_000_000)

    return i


def profile_queue(queue: mp.Queue, name: str) -> None:
    profile = DatasetProfile()

    handled = 0
    while True:
        start = perf_counter()
        csv_bytes: bytes = queue.get()
        df = pd.read_csv(io.BytesIO(csv_bytes))
        # profile.track(df)
        end = perf_counter()
        handled = handled + 1
        _fake_work()
        print(f"[QUEUE {name}] done with {handled} of size {len(df)} in {end-start}s")


def profile_pipe(conn: Connection, name: str) -> None:
    profile = DatasetProfile()

    handled = 0
    # while True:
    #     start = perf_counter()
    #     csv_bytes: bytes = conn.recv()
    #     df = pd.read_csv(io.BytesIO(csv_bytes))
    #     # profile.track(df)
    #     end = perf_counter()
    #     handled = handled + 1
    #     _fake_work()
    #     print(f"[PIPE {name}] done with {handled} of size {len(df)} in {end-start}s")
