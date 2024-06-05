import asyncio
from bleak import BleakScanner, BleakClient

 
class BLDevice:
    def __init__(self, name: str):
        self.name = name
        self.client = None
        self.characteristic_uuid = None

    async def connect(self):
        if not self.client or not self.client.is_connected:
            print(f"Trying to connect to {self.name} device...")
            device = await BleakScanner.find_device_by_name(self.name, timeout=20.0)
            if device is None:
                raise Exception(f"Device with name {self.name} not found.")
            self.client = BleakClient(device)
            await self.client.connect()
            print(f"Connected to {self.name}")
            await self.client.pair()
            print(f"Paired with {self.name}")

    async def get_writable_char_uuid(self):
        await self.connect()
        if not self.characteristic_uuid:
            for service in self.client.services:
                for char in service.characteristics:
                    properties = set(char.properties)
                    # in current circumstanse (original HM-10 ble module with latest firmware), 
                    # in this way we can find a RX/TX characteristic uuid
                    if properties.issuperset({'read', 'write-without-response', 'write', 'notify', 'indicate'}):
                        self.characteristic_uuid = char.uuid
                        print(f"Found writable characteristic: {char.uuid}")
            if not self.characteristic_uuid:
                raise Exception("No writable characteristic found.")
        return self.characteristic_uuid

    async def write(self, message):
        await self.connect()
        try:
            await self.client.write_gatt_char(
                await self.get_writable_char_uuid(), 
                message.encode('utf-8')
            )
        except Exception as e:
            print("Got an error while writing: ", e)
            return
        print(f"Message '{message}' written to characteristic {self.characteristic_uuid}")

    async def disconnect(self):
        if self.client and self.client.is_connected:
            await self.client.disconnect()
            print(f"Disconnected from {self.name}")

if __name__ == '__main__':
    NAME = "FBT(@Dr00L)"

    my_device = BLDevice(NAME)
    loop = asyncio.get_event_loop()

    # Write to the characteristic
    loop.run_until_complete(my_device.write("hello world!"))

    # Disconnect (optional, good practice to disconnect when done)
    loop.run_until_complete(my_device.disconnect())
