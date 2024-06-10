import asyncio
from ble_server import BLEServer


if __name__ == '__main__':
    ble_server = BLEServer()
    asyncio.run(ble_server.run())
