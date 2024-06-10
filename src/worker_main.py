import asyncio
from worker import Worker
from environment import redis_conn


if __name__ == '__main__':
    worker = Worker('rawdata_queue', redis_conn)
    asyncio.run(worker.run())
