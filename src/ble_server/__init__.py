import asyncio
from ble_server.ble import BLEDevice
from ble_server.msg import MessageBroker


class BLEServer:
    def __init__(self):
        self.device = BLEDevice()
        self.message_broker = MessageBroker()
        self.device.set_message_broker(self.message_broker)

    async def run(self):
        await self.device.write("Successfully connected from Server !")
        await self.device.start_char_notify_handle()

        print("\n\nPress Ctrl-C to exit...\n\n")
        try:
            while True:
                if not self.device.has_connection:
                    raise KeyboardInterrupt
                await asyncio.sleep(0.0001)
        except KeyboardInterrupt:
            await self.device.disconnect()
