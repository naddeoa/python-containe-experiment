import concurrent.futures as cf
import multiprocessing as mp
from time import perf_counter
from random import randint

profiling_queue: mp.Queue = mp.Queue()


# do stuff on the cpu for a second
def _profile_cpu() -> int:
    i = 0
    start = perf_counter()

    while (perf_counter() - start) < 1:
        i = i + randint(0, 1_000_000)

    return i


def profile_mp(queue: mp.Queue) -> None:
    i = 0
    log = open("/tmp/log.txt", "w")
    log.write("start\n")

    while True:
        item: int = queue.get()
        i = i + item
        _profile_cpu()
        log.write(f'{i}\n')
        log.flush()
