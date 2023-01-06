import concurrent.futures as cf
import multiprocessing as mp

import uvicorn

from .profiling import profile_mp, profiling_queue

if __name__ == "__main__":
    # mp.set_start_method('spawn')
    print("starting up profiling process")
    process = mp.Process(target=profile_mp, args=(profiling_queue,))
    process.start()
    print("Joined")

    config = uvicorn.Config("ai.whylabs.container.main:app", port=8000, reload=True, log_level="debug")
    server = uvicorn.Server(config)
    server.run()
    process.join()
