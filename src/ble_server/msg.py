import json
import asyncio
import re
from environment import settings, redis_conn


class MessageBroker:
    def __init__(self):
        self.message_buffer = ""  # buffer for assembling complete message
        self.collecting_message = False  # Is collecting message

    async def handle_notification(self, data):
        """Asssembling complete message from incoming notifications"""
        if data == '~RAWDATASTART~':
            self.message_buffer = ""
            self.collecting_message = True
        elif data == '~RAWDATAEND~':
            self.collecting_message = False
            complete_message = self.message_buffer
            self.message_buffer = ""
            # print(f"Complete message received: {complete_message}")
            asyncio.create_task(self.parse_message(complete_message))
        elif self.collecting_message:
            self.message_buffer += data
        else:
            # irrelevant messages
            pass
    async def parse_message(self, message):
        """Parsing of complete message"""
        # like "A:-0.104492|0.028564|0.938477G:0.251115|-4.466728|0.939697:T:32.5:"
        pattern = r'([A-Z]):(-?\d+(?:\.\d+)?(?:\|-?\d+(?:\.\d+)?)*):'

        try:
            matches = re.findall(pattern, message)
            result = {}
            for match in matches:
                key = match[0]
                values = [float(val) for val in match[1].split('|')]
                result[key] = values
            await redis_conn.lpush('rawdata_queue', json.dumps(result)) 
        except:
            pass