import concurrent.futures as cf
import multiprocessing as mp

import uvicorn

from .profiling import pipe_rcv, profile_pipe, profile_queue, queue


def foo() -> None:
    import io

    import pandas as pd
    from whylogs.core import DatasetProfile
    file = open('/home/anthony/workspace/python-whylogs-container/data/short-data.csv', 'rb')
    csv = file.read()
    print(type(csv))

    print("starting")
    profile = DatasetProfile()
    b = io.BytesIO(csv)
    print("about to decode bytes")
    df = pd.read_csv(b, encoding="utf8")
    profile.track(df)
    print(str(profile.view().to_pandas()))


def create_queue_profiler(name: str) -> mp.Process:
    # mp.set_start_method('spawn')
    print(f"starting up queue profiler {name}")
    process = mp.Process(target=profile_queue, args=(queue,name,), daemon=True)
    process.start()
    print("Joined")
    return process

def create_pipe_profiler(name: str) -> mp.Process:
    # mp.set_start_method('spawn')
    print(f"starting up pipe profiler {name}")
    process = mp.Process(target=profile_pipe, args=(pipe_rcv,name,), daemon=True)
    process.start()
    print("Joined")
    return process

if __name__ == "__main__":
    # foo()
    queue_workers = 1
    pipe_workers = 1

    processes = []
    for i in range(queue_workers):
        processes.append(create_queue_profiler(str(i)))

    for i in range(pipe_workers):
        processes.append(create_pipe_profiler(str(i)))

    config = uvicorn.Config("ai.whylabs.container.main:app", port=8000, reload=True, log_level="debug")
    server = uvicorn.Server(config)
    server.run()

    for p in processes:
        p.join()
