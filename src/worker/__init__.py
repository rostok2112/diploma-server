import json
import asyncio
from worker.tasks import *


QUEUE_TO_TASK_MAPPING = {
    'rawdata_queue': process_complementary_filter
}

class Worker:
    def __init__(self, queue_name, redis_conn):
        self.queue_name = queue_name
        self.redis_conn = redis_conn
        

    async def process_task(self, task_data):
        # print(f"Processing task: {task_data}")
        try:
            await QUEUE_TO_TASK_MAPPING[self.queue_name](task_data, self.redis_conn)
        except Exception as e:
            pass

    async def run(self):
        await self.redis_conn.flushall()
        print("\n\nPress Ctrl-C to exit...\n\n")
        while True:
            task_data = await self.redis_conn.brpop(self.queue_name)
            task_data = task_data[1]
            task_data = json.loads(task_data)
            await self.process_task(task_data)
            await asyncio.sleep(0.0001)
