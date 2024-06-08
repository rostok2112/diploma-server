import asyncio
from bleak import BleakScanner, BleakClient
from bleak.backends.characteristic import BleakGATTCharacteristic
import settings

 
class BLDevice:
    def __init__(self, name: str = settings.FBT_MODULE_NAME):
        self.name = name
        self.client = None
        self.characteristic_uuid = None

    
    @property
    def has_connection(self) -> bool:
        return self.client and self.client.is_connected
        
    async def connect(self):
        if not self.has_connection:
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
                    # in this way we can find a Rx/Tx characteristic uuid
                    if properties.issuperset({'read', 'write-without-response', 'write', 'notify', 'indicate'}):
                        self.characteristic_uuid = char.uuid
                        print(f"Found writable characteristic: {char.uuid}")
            if not self.characteristic_uuid:
                raise Exception("No writable characteristic found.")
        return self.characteristic_uuid

    async def start_char_notify_handle(self):
        def notify_handler(charact: BleakGATTCharacteristic, data: bytearray):
            """Simple notification handler which prints the data received."""
            print(f"Got notification about change of `{charact.description}` characteristic({charact.uuid}): `{data}`")
        print(f"Starting notification handle from characteristic({await self.get_writable_char_uuid()})")
        
        await self.client.start_notify(
            self.characteristic_uuid, 
            notify_handler
        )
        
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
        print(f"Message '{message}' written to characteristic({self.characteristic_uuid})")

    async def disconnect(self):
        if self.has_connection:
            await self.client.stop_notify(
                await self.get_writable_char_uuid()
            )
            await self.client.disconnect()
            print(f"Disconnected from {self.name}")

async def main():
    my_device = BLDevice()
    
    await my_device.write("Successfully connected from Server !")
    await my_device.start_char_notify_handle()
    
    print("\n\nPress Ctrl-C to exit...\n\n")
    try:
        while True:
            if not my_device.has_connection:
                raise KeyboardInterrupt
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        await my_device.disconnect()

if __name__ == '__main__':
    asyncio.run(main())
